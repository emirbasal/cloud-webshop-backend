
preset_headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Credentials': 'true',
    }


class Response:

    def __init__(self, statusCode, body):
        self.headers = preset_headers
        self.statusCode = statusCode
        self.body = body

    def to_json(self):
        return {
            'headers': self.headers,
            "statusCode":  self.statusCode,
            "body": self.body
        }
