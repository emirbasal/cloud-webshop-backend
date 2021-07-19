import json
from src.main.functions.helper.Response import Response
from src.main.persistence import db_service
from datetime import datetime, timedelta
import jwt
import os
import bcrypt
import logging

JWT_EXP_DELTA_SECONDS = 60


def auth_user(event, context):
    table = db_service.get_table("USERS_TABLE")
    received_data = json.loads(event['body'])

    user_exists, user = db_service.does_user_exist(received_data['username'], table)

    response = Response(statusCode=200, body={'token': ''})

    if user_exists:
        logging.warning(user['password'].encode())
        logging.warning(received_data['password'].encode())
        password_hash = user['password'].encode()
        received_password = received_data['password'].encode()
        if bcrypt.checkpw(received_password,  password_hash):
            payload = {
                'user_id': user['username'],
                'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
            }
            jwt_token = jwt.encode(payload, os.environ['JWT_SECRET'], os.environ['JWT_ALGORITHM'])

            response = Response(statusCode=200, body={'token': jwt_token})

    return response.to_json()
