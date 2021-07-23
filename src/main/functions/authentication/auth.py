import json
import jwt
import os
import bcrypt
from src.main.helper.classes.response import Response
from src.main.helper.services import db_service
from datetime import datetime, timedelta


def auth_user(event, context):
    jwt_exp_seconds = os.environ['JWT_EXP_SECONDS']

    table = db_service.get_users_table()
    received_data = json.loads(event['body'])

    user_exists, user = db_service.does_user_exist(received_data['username'], table)

    response = Response(statusCode=200, body={'token': ''})

    if user_exists:
        password_hash = user['password'].encode()
        received_password = received_data['password'].encode()
        if bcrypt.checkpw(received_password,  password_hash):
            payload = {
                'user_id': user['username'],
                'exp': datetime.utcnow() + timedelta(seconds=int(jwt_exp_seconds))
            }
            jwt_token = jwt.encode(payload, os.environ['JWT_SECRET'], os.environ['JWT_ALGORITHM'])

            response = Response(statusCode=200, body={'token': jwt_token})

    return response.to_json()
