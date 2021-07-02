import json
import logging
import time
import uuid
import boto3
from decimal import Decimal
from src.functions import decimalencoder, lambda_helper
from src.persistence import db_service

client = boto3.client('lambda')


def create_order(event, context):

    data = json.loads(event['body'])
    logging.warning(data)
    if not is_data_valid(data):
        logging.error("Validation Failed. Attribute(s) are missing. Couldn't create the order.")
        response = {
            "statusCode": 400,
            "body": json.dumps(
                {"message": "Validation Failed. Attribute(s) are missing. Couldn't create the order."}
            )
        }
        return response

    arn = lambda_helper.get_arn('payment')
    logging.warning(arn)
    test_response = client.invoke(
        FunctionName=arn,
        InvocationType='RequestResponse',
        Payload=json.dumps(json.loads(event['body']))
    )

    timestamp = str(time.time())
    table = db_service.get_orders_table()

    item = {
        'id': str(uuid.uuid1()),
        'amount': Decimal(str(data['amount'])),
        'currency': data['currency'],
        'invoice:': 'invoice',
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


def is_data_valid(data):

    return False
