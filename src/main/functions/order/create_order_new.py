import json
import time
import uuid
import boto3
from src.main.functions.helper import lambda_helper
from src.main.functions.helper.Response import Response
from src.main.persistence import db_service



def create_order(event, context):
    client = boto3.client('lambda')
    order = json.loads(event['body'])
    if not is_data_valid(order):
        response = Response(statusCode=400, body={"message": "Validation Failed. Attribute(s) are missing. Couldn't "
                                                             "create the order."})
        return response.to_json()

    order = create_order_for_paymentAPI(order)
    if not order['items']:
        response = Response(statusCode=400, body={"message": "Product(s) can not be found in database"})
        return response.to_json()

    items = order['items']
    arn = lambda_helper.get_arn('payment')
    payment_response = client.invoke(
        FunctionName=arn,
        InvocationType='RequestResponse',
        Payload=json.dumps(order)
    )

    if payment_response['StatusCode'] != 200:
        response = Response(statusCode=400, body={"message": "Error from Payment-API. Please try again",
                                                  "Error": payment_response})

        return response.to_json()

    payload = payment_response['Payload']
    data = payload.read()

    order = json.loads(data)
    order['createdAt'] = str(time.time())
    order['items'] = items

    table = db_service.get_orders_table()
    table.put_item(Item=order)
    response = Response(statusCode=200, body=order)

    return response.to_json()


def is_data_valid(data):
    if 'email' in data and 'items' in data and 'status' in data and 'card' in data:
        if data['email'] and data['items'] and data['status'] and data['card']['number']:
            return True
    return False


def create_order_for_paymentAPI(order):
    order['id'] = str(uuid.uuid1())
    order['items'] = lookup_items(order['items'])
    order['amount'] = calc_amount(order['items'])
    # TODO: Make globally changable
    order['currency'] = 'EUR'
    return order


def lookup_items(products_from_request):
    all_products = []
    products_table = db_service.get_products_table()
    for product_from_request in products_from_request:
        does_exist, product = db_service.does_item_exist(product_from_request['id'], products_table)
        if not does_exist:
            return []
        product_from_request['amount'] = int(product['amount']) * product_from_request['quantity']
        product_from_request['description'] = product['name']
        product_from_request['currency'] = product['currency']

        all_products.append(product_from_request)

    return all_products


def calc_amount(products_of_order):
    amount_sum = 0
    for product in products_of_order:
        amount_sum += product['amount']

    return amount_sum
