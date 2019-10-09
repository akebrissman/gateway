"""
This file (test_models.py) contains the unit tests for the models.py file.
"""


def test_new_user(new_fb):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed_password, authenticated, and role fields are defined correctly
    """
    assert new_fb.imsi == '123456789012345'
    assert new_fb.token == 'guid'
