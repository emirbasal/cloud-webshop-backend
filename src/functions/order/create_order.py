import json
import time
import uuid
import boto3
from src.functions.helper import lambda_helper
from src.functions.helper.Response import Response
from src.persistence import db_service


client = boto3.client('lambda')


def create_order(event, context):

    order = json.loads(event['body'])
    if not is_data_valid(order):
        response = Response(statusCode=400, body={"message": "Validation Failed. Attribute(s) are missing. Couldn't "
                                                             "create the order."})

        return response.to_json()

    new_id = str(uuid.uuid1())
    order["id"] = new_id
    arn = lambda_helper.get_arn('payment')
    payment_response = client.invoke(
        FunctionName=arn,
        InvocationType='RequestResponse',
        Payload=json.dumps(order)
    )
    # logging.warning(payment_response)

    if payment_response['StatusCode'] != 200:
        response = Response(statusCode=400, body={"message": "Error from Payment-API. Please try again"})

        return response.to_json()

    payload = payment_response['Payload']
    data = payload.read()

    order = json.loads(data)
    order['createdAt'] = str(time.time())
    table = db_service.get_orders_table()

    table.put_item(Item=order)
    response = Response(statusCode=200, body=order)

    return response.to_json()


def is_data_valid(data):
    if ('amount' in data and 'currency' in data and 'email' in data
            and 'items' in data and 'status' in data and 'card' in data):

        if (data['amount'] and data['currency'] and data['email'] and data['items']
                and data['status'] and data['card']['number']):

            return True
    return False
