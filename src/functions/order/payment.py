import json
import logging
import os
import requests
import time
import uuid
from decimal import Decimal
from src.functions import decimalencoder, lambda_helper
from src.persistence import db_service


def payment(event, context):

    # data = json.loads(event)

    logging.warning(event)

    url = os.environ('PAYMENT_API')
    headers = {'Content-type': 'application/json', 'api_key': os.environ('API_KEY')}
    response = requests.post(url, data=json.dumps(event), headers=headers)

    logging.warning('---------------')
    logging.warning(response)

    return response
