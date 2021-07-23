import jwt
import os


def is_authenticated(request):
    if 'Authorization' in request['headers'] and request['headers']['Authorization']:
        authorization = request['headers']['Authorization']
        token = get_token(authorization)
        return verify_token(token)
    return False


def verify_token(token):
    try:
        payload = jwt.decode(token, os.environ['JWT_SECRET'],
                             algorithms=[os.environ['JWT_ALGORITHM']])
    except (jwt.DecodeError, jwt.ExpiredSignatureError):
        return False

    return True


def get_token(token):
    if "Bearer " in token:
        return token.split("Bearer ")[1]
    return ''
