import json
import time
import boto3
from src.main.helper.services import external_resource_service, db_service
from src.main.helper.classes.response import Response


def create_order(event, context):
    client = boto3.client('lambda')
    order_from_request = json.loads(event['body'])
    if not is_data_valid(order_from_request):
        response = Response(statusCode=400, body={"message": "Validation Failed. Attribute(s) are missing. Couldn't "
                                                             "create the order."})
        return response.to_json()

    arn = external_resource_service.get_arn('payment')
    payment_response = client.invoke(
        FunctionName=arn,
        InvocationType='RequestResponse',
        Payload=json.dumps(order_from_request)
    )

    if payment_response['StatusCode'] != 200:
        response = Response(statusCode=400, body={"message": "Error from Payment-API. Please try again",
                                                  "Error": payment_response})

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
    if 'email' in data and 'items' in data and 'status' in data and 'card' in data and 'address' in data:
        if (data['email'] and data['items'] and data['status'] and data['card']['number']
                and data['address']['address1'] and data['address']['address2'] and data['address']['city']
                and data['address']['country']):
            return True
    return False
