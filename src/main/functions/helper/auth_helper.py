import logging
import jwt
import os


def verify_token(jwt_token):
    try:
        payload = jwt.decode(jwt_token, os.environ['JWT_SECRET'],
                             algorithms=[os.environ['JWT_ALGORITHM']])
        logging.warning(payload)
    except (jwt.DecodeError, jwt.ExpiredSignatureError):
        return False

    return True
