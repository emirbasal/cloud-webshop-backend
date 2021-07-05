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

    order = json.loads(event['body'])
    if not is_data_valid(order):
        logging.error("Validation Failed. Attribute(s) are missing and/or are Empty. Couldn't create the order.")
        response = {
            "statusCode": 400,
            "body": json.dumps(
                {"message": "Validation Failed. Attribute(s) are missing. Couldn't create the order."}
            )
        }
        return response

    new_id = str(uuid.uuid1())
    order["id"] = new_id
    arn = lambda_helper.get_arn('payment')
    response = client.invoke(
        FunctionName=arn,
        InvocationType='RequestResponse',
        Payload=json.dumps(order)
    )
    payload = response['Payload']
    data = payload.read()

    order = json.loads(data)
    order['createdAt'] = str(time.time())
    table = db_service.get_orders_table()

    table.put_item(Item=order)

    response = {
        "statusCode": 200,
        "body": json.dumps(order,
                           cls=decimalencoder.DecimalEncoder)
    }

    return response


def is_data_valid(data):
    if ('amount' in data and 'currency' in data and 'email' in data
            and 'items' in data and 'status' in data and 'card' in data):

        if (data['amount'] and data['currency'] and data['email'] and data['items']
                and data['status'] and data['card']['number']):

            return True
    return False
