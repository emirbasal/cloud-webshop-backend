import json
from src.main.helper.services import external_resource_service
import urllib3


def payment(event, context):
    payment_endpoint, header = external_resource_service.get_payment_api()

    http = urllib3.PoolManager()
    response = http.request('POST', payment_endpoint, body=json.dumps(event), headers=header, retries=False)

    response = json.loads(response.data)
    return response
