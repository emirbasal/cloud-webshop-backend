import json
from src.functions.helper import decimalencoder

preset_headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Credentials': 'true',
    'Access-Control-Allow-Methods': '*',
    'Content-Type': 'application/json'
    }


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
