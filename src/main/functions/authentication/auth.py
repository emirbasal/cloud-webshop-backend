import json
from src.main.functions.helper.Response import Response
from src.main.persistence import db_service
from src.main.functions.helper.auth_helper import verify_token
from datetime import datetime, timedelta
import jwt
import os


JWT_EXP_DELTA_SECONDS = 3600


def auth_user(event, context):
    table = db_service.get_table("USERS_TABLE")
    received_data = json.loads(event['body'])

    user_exists, user = db_service.does_user_exist(received_data['username'], table)

    if user_exists:
        if user['password'] == received_data['password']:
            payload = {
                'user_id': user['username'],
                'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
            }
            jwt_token = jwt.encode(payload, os.environ['JWT_SECRET'], os.environ['JWT_ALGORITHM'])

            response = Response(statusCode=200, body={'token': jwt_token})
        else:
            response = Response(statusCode=200, body={'Message': 'Wrong password'})

    else:
        response = Response(statusCode=404, body={'Message': 'User not found'})

    return response.to_json()


# TODO: REMOVE
def auth_verify(event, context):
    received_data = json.loads(event['body'])
    token = received_data['token']
    if token:
        is_token_valid = verify_token(token)

        response = Response(statusCode=200, body={'Message': is_token_valid})
    else:
        response = Response(statusCode=404, body={'Message': 'User not found'})

    return response.to_json()
