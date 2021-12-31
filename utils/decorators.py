import os
import json

from dotenv import load_dotenv, find_dotenv
from functools import wraps
from urllib.request import urlopen
from flask import request, _request_ctx_stack, abort, Response
from jose import jwt

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

config = {
    "DOMAIN": os.getenv("AUTH_DOMAIN", "your.domain.com"),
    "AUDIENCE": os.getenv("AUTH_API_AUDIENCE", "your.audience.com"),
    "ALGORITHMS": os.getenv("AUTH_ALGORITHMS", "RS256"),
}


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


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
    """Validates an Access Token"""

    rsa_key = None
    public_key = os.getenv("AUTH_PUBLIC_KEY")
    if not public_key:
        # Let's find our publicly available public keys,
        # which we'll use to validate the token's signature
        jsonurl = urlopen("https://" + config["DOMAIN"] + "/.well-known/jwks.json")
        jwks = json.loads(jsonurl.read())
    else:
        if public_key[:1] == "{":
            rsa_key = json.loads(public_key)
        else:
            rsa_key = public_key

    # We will parse the token and get the header for later use
    unverified_header = jwt.get_unverified_header(token)

    # Check if the token has a key ID
    if "kid" not in unverified_header:
        payload = {
            "code": "missing_kid",
            "description": "No kid found in token"
        }
        raise AuthError(payload, 401)

    try:
        if not rsa_key:
            # Check if we have a key with the key ID specified
            # from the header available in our list of public keys
            rsa_key = next(
                key for key in jwks["keys"]
                if key["kid"] == unverified_header["kid"]
            )

        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=config["ALGORITHMS"],
                audience=config["AUDIENCE"],
                issuer="https://" + config["DOMAIN"] + "/",
            )

            # Verify that the requested scope exist in the token
            token_scope = payload.get('scope').split(' ')
            if scope and scope not in token_scope:
                payload = {
                    "code": "missing_scope",
                    "description": "No matching scope found in token"
                }
                raise AuthError(payload, 401)

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
                "description": "Unable to parse authentication token.",
            }
            raise AuthError(payload, 401)

    except StopIteration:
        # We did not find the key with the ID specified in the token's header
        # in the list of available public keys for our Auth0 tenant.
        payload = {
            "code": "invalid_header",
            "description": "No valid public key found to validate signature.",
        }
        raise AuthError(payload, 401)


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
            # Abort the request if something went wrong fetching the token
            # or validating the token.
            # We return the status from the raised error,
            # and return the error as a json response body
            return abort(Response(json.dumps(error.error), error.status_code))

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
                # Abort the request if something went wrong fetching the token
                # or validating the token.
                # We return the status from the raised error,
                # and return the error as a json response body
                return abort(Response(json.dumps(error.error), error.status_code))

            return f(*args, **kwargs)

        return wrapped

    return inner_decorator
