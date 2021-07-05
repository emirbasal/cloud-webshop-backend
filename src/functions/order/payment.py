import json
import logging
from src.functions import lambda_helper
import urllib3



def payment(event, context):
    payment_endpoint, header = lambda_helper.get_payment_api()

    http = urllib3.PoolManager()
    response = http.request('POST', payment_endpoint, body=json.dumps(event), headers=header, retries=False)

    if response.status != 200:
        logging.error("Could not get payment information from payment API")
        #TODO: RETRY

    logging.warning('Rechnung wurde erfolgreich erhalten')
    logging.warning(json.loads(response.data))
    response = json.loads(response.data)
    return response
