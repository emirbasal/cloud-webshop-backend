import json
from src.main.helper.classes import decimalencoder
import os


preset_headers = {
    'Access-Control-Allow-Origin': os.environ['FRONTEND_ORIGIN'],
    'Access-Control-Allow-Credentials': 'true',
    'Access-Control-Allow-Methods': '*',
    'Content-Type': 'application/json'
    }


# Response class which generalizes sent responses for all lambda functions
class Response:

    def __init__(self, statusCode, body):
        self.headers = preset_headers
        self.statusCode = statusCode
        self.body = body

    def to_json(self):
        response = {
            "headers": self.headers,
            "statusCode":  self.statusCode,
            "body": json.dumps(self.body, cls=decimalencoder.DecimalEncoder)
        }
        return response
