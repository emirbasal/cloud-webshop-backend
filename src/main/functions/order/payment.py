import json
from src.main.functions.helper import lambda_helper
import urllib3


def payment(event, context):
    payment_endpoint, header = lambda_helper.get_payment_api()

    http = urllib3.PoolManager()
    response = http.request('POST', payment_endpoint, body=json.dumps(event), headers=header, retries=False)

    response = json.loads(response.data)
    return response
