import os
import json
import datetime as dt

from dotenv import load_dotenv, find_dotenv
from functools import wraps
from urllib.request import urlopen
from flask import request, _request_ctx_stack, abort, jsonify
from jose import jwt

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

config = {
    "DOMAIN": os.getenv("AUTH_DOMAIN", "your.domain.com"),
    "ISSUER": "https://" + os.getenv("AUTH_DOMAIN") + "/",
    "AUDIENCE": os.getenv("AUTH_API_AUDIENCE", "your.audience.com"),
    "ALGORITHMS": os.getenv("AUTH_ALGORITHMS", "RS256"),
}


g_cached_keys_per_kid = {}
g_requests_per_minute = 5
g_requests_count = 0
g_current_rate_time = ""


class AuthError(Exception):
    def __init__(self, error: dict, status_code: int):
        self.error = error
        self.status_code = status_code


def is_unittest() -> bool:
    return "AUTH_PUBLIC_KEY" in os.environ


def override_env() -> str:
    rsa_key = os.getenv("AUTH_PUBLIC_KEY")
    config["DOMAIN"] = os.getenv("AUTH_DOMAIN")
    config["ISSUER"] = "https://" + os.getenv("AUTH_DOMAIN") + "/"
    config["AUDIENCE"] = os.getenv("AUTH_API_AUDIENCE")
    config["ALGORITHMS"] = os.getenv("AUTH_ALGORITHMS", "RS256")

    return rsa_key


def update_rate_limit():
    """Increase the counter if it is within the same minute else set it to 1"""
    global g_current_rate_time
    global g_requests_count
    time_str = dt.datetime.now().isoformat(timespec="minutes")
    if time_str != g_current_rate_time:
        g_current_rate_time = time_str
        g_requests_count = 1
    else:
        g_requests_count += 1


def is_within_rate_limit() -> bool:
    """
    Return True if this request is in another minute then the previous
    or if there are less then g_jwks_requests_per_minute for the current minute
    """

    time_str = dt.datetime.now().isoformat(timespec="minutes")
    return (time_str != g_current_rate_time) or \
           (time_str == g_current_rate_time and g_requests_count < g_requests_per_minute)


def get_token() -> str:
    """Obtains the Access Token from the Authorization Header"""

    # Get the authorization header
    authorization_header = request.headers.get("Authorization", None)

    # Raise an error if no Authorization error is found
    if not authorization_header:
        payload = {
            "code": "authorization_header_missing",
            "description": "Authorization header is expected",
        }
        raise AuthError(payload, 401)

    authorization_header_parts = authorization_header.split()

    # We are expecting the Authorization header to contain a Bearer token
    if authorization_header_parts[0].lower() != "bearer":
        payload = {
            "code": "invalid_header",
            "description": "Authorization header must be a Bearer token",
        }
        raise AuthError(payload, 401)

    # The Authorization header is prefixed with Bearer, but does not contain the actual token
    elif len(authorization_header_parts) == 1:
        payload = {"code": "invalid_header", "description": "Token not found"}
        raise AuthError(payload, 401)

    # We only expect 2 parts, "Bearer" and the access token
    elif len(authorization_header_parts) > 2:
        payload = {
            "code": "invalid_header",
            "description": "Authorization header must be a valid Bearer token",
        }
        raise AuthError(payload, 401)

    # If all checks out, we return the access token
    return authorization_header_parts[1]


def validate_token(token: str, scope: str = None):
    """Validates an Access Token

    Caching
    By default, signing key verification results are cached in order to prevent excessive HTTP requests to the JWKS endpoint. 
    If a signing key matching the kid is found, this will be cached and the next time this kid is requested the signing key will be served from the cache. 
    
    Rate Limiting
    Even if caching is enabled the function will call the JWKS endpoint if the kid is not available in the cache, because a key rotation could have taken place.
    To prevent attackers to send many random kids there is a rate limiting
    This limit the number of calls that are made to the JWKS endpoint per minute (because it would be highly unlikely that signing keys are rotated multiple times per minute).
    """

    # We will parse the token and get the header for later use
    unverified_token_header = jwt.get_unverified_header(token)

    # Check if the token has a key ID
    if "kid" not in unverified_token_header:
        payload = {
            "code": "missing_kid",
            "description": "No kid found in token"
        }
        raise AuthError(payload, 401)

    rsa_key = None
    token_kid = unverified_token_header["kid"]
    if token_kid not in g_cached_keys_per_kid and is_within_rate_limit():
        if is_unittest():
            rsa_key = override_env()
            g_cached_keys_per_kid[token_kid] = rsa_key
        else:
            # Let's fetch the public key, from the authentication domain,
            # which we'll use to validate the token's signature
            url = urlopen("https://" + config["DOMAIN"] + "/.well-known/jwks.json")
            jwks = json.loads(url.read())

            # Check if we have a key with the key ID specified
            # from the header available in our list of public keys
            for key in jwks["keys"]:
                if key["kid"] == token_kid:
                    rsa_key = key
                    g_cached_keys_per_kid[token_kid] = key
                    break

        update_rate_limit()
        print("Key fetched from auth domain")
    else:
        rsa_key = g_cached_keys_per_kid.get(token_kid)
        print("Key found in cache")

    try:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=config["ALGORITHMS"],
                audience=config["AUDIENCE"],
                issuer=config["ISSUER"],
            )

            _request_ctx_stack.top.current_user = payload

        # The token is not valid if the expiry date is in the past
        except jwt.ExpiredSignatureError:
            raise AuthError(
                {"code": "token_expired", "description": "Token is expired"},
                401
            )

        # The token should be issued by our Auth0 tenant,
        # and to be used with our API (Audience)
        except jwt.JWTClaimsError:
            payload = {
                "code": "invalid_claims",
                "description":
                    "Incorrect claims, please check the audience and issuer",
            }
            raise AuthError(payload, 401)

        # The token's signature is invalid
        except jwt.JWTError:
            payload = {
                "code": "invalid_signature",
                "description": "The signature is not valid",
            }
            raise AuthError(payload, 401)

        # Something went wrong parsing the JWT
        except Exception:
            payload = {
                "code": "invalid_header",
                "description": "Unable to parse authentication token",
            }
            raise AuthError(payload, 401)

        # Verify that the requested scope exist in the token
        token_scope = payload.get('scope').split(' ')
        if scope is not None and scope not in token_scope:
            payload = {
                "code": "missing_scope",
                "description": "No matching scope found in token"
            }
            raise AuthError(payload, 401)

    except StopIteration:
        # We did not find the key with the ID specified in the token's header
        # in the list of available public keys for our Auth0 tenant.
        payload = {
            "code": "invalid_header",
            "description": "No valid public key found to validate signature",
        }
        raise AuthError(payload, 401)


def json_response(status_code, data=None):
    response = jsonify(data or {'error': 'There was an error'})
    response.status_code = status_code
    return response


def requires_auth(f):
    """Determines if there is a valid Access Token available"""

    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            # Lets get the access token from the Authorization header
            token = get_token()

            # Once we have the token, we can validate it
            validate_token(token)
        except AuthError as error:
            # Abort the request if something went wrong fetching the token or validating the token.
            # We return the status from the raised error, and return the error as a json response body
            # When running the tests a more detailed error is returned that we don't want to show in production
            if "PYTEST_CURRENT_TEST" in os.environ:
                return abort(json_response(error.status_code, error.error))
            else:
                print(error.status_code, error.error)
                return abort(json_response(error.status_code, {'description': 'Authentication Error'}))

        return f(*args, **kwargs)

    return decorated


def requires_auth_with_scope(scope: str = None):
    def inner_decorator(f):
        def wrapped(*args, **kwargs):
            try:
                # Lets get the access token from the Authorization header
                token = get_token()

                # Once we have the token, we can validate it
                validate_token(token, scope)
            except AuthError as error:
                # Abort the request if something went wrong fetching the token or validating the token.
                # We return the status from the raised error, and return the error as a json response body
                # When running the tests a more detailed error is returned that we don't want to show in production
                if "PYTEST_CURRENT_TEST" in os.environ:
                    return abort(json_response(error.status_code, error.error))
                else:
                    print(error.status_code, error.error)
                    return abort(json_response(error.status_code, {'description': 'Authentication Error'}))

            return f(*args, **kwargs)

        return wrapped

    return inner_decorator
