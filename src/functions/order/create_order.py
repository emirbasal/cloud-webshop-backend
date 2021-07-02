import json
import logging
import time
import uuid
import logging
from decimal import Decimal
from src.functions import decimalencoder, lambda_helper
from src.persistence import db_service



def create_order(event, context):
    arn = lambda_helper.get_arn('create-order')

    data = json.loads(event['body'])
    if 'amount' not in data or 'currency' not in data or 'items' not in data or 'email' not in data \
            or 'status' not in data or 'cardNumber' not in data:
        logging.error("Validation Failed. Attribute(s) are missing. Couldn't create the order.")

        response = {
            "statusCode": 400,
            "body": json.dumps(
                {"message": "Validation Failed. Attribute(s) are missing. Couldn't create the order."}
            )
        }
        return response

    timestamp = str(time.time())
    table = db_service.get_orders_table()

    item = {
        'id': str(uuid.uuid1()),
        'amount': Decimal(str(data['amount'])),
        'currency': data['currency'],
        'items': data['items'],
        'email': data['email'],
        'status': data['status'],
        'cardNumber': data['cardNumber'],
        'createdAt': timestamp,
    }

    table.put_item(Item=item)

    response = {
        "statusCode": 200,
        "body": json.dumps(item,
                           cls=decimalencoder.DecimalEncoder)
    }

    return response
