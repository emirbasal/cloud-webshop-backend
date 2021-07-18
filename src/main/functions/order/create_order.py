import json
import time
import uuid
import boto3
from src.main.functions.helper import lambda_helper
from src.main.functions.helper.Response import Response
from src.main.functions.helper.decimalencoder import DecimalEncoder
from src.main.persistence import db_service
import logging


def create_order(event, context):
    client = boto3.client('lambda')
    order_from_request = json.loads(event['body'])
    if not is_data_valid(order_from_request):
        response = Response(statusCode=400, body={"message": "Validation Failed. Attribute(s) are missing. Couldn't "
                                                             "create the order."})
        return response.to_json()

    order_for_payment_api = create_order_for_payment_api(order_from_request)
    if not order_for_payment_api['items']:
        response = Response(statusCode=400, body={"message": "Product(s) can not be found in database"})
        return response.to_json()

    arn = lambda_helper.get_arn('payment')
    payment_response = client.invoke(
        FunctionName=arn,
        InvocationType='RequestResponse',
        Payload=json.dumps(order_for_payment_api)
    )

    if payment_response['StatusCode'] != 200:
        response = Response(statusCode=400, body={"message": "Error from Payment-API. Please try again",
                                                  "Error": payment_response})

        return response.to_json()

    payload = payment_response['Payload']
    data = payload.read()
    order = json.loads(data)
    order['createdAt'] = str(time.time())
    order['items'] = order_from_request['items']
    order['address'] = order_from_request['address']

    table = db_service.get_orders_table()
    table.put_item(Item=order)
    response = Response(statusCode=200, body=order)

    # Publishing to sns topic to get delivery status and information
    response_from_sns = publish_to_sns_delivery(order)
    logging.warning(response_from_sns)

    return response.to_json()


def is_data_valid(data):
    if 'email' in data and 'items' in data and 'status' in data and 'card' in data and 'address' in data:
        if (data['email'] and data['items'] and data['status'] and data['card']['number']
                and data['address']['address1'] and data['address']['address2'] and data['address']['city']
                and data['address']['country']):
            return True
    return False


def create_order_for_payment_api(order):
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


def publish_to_sns_delivery(order):
    products = get_products_for_sns(order['items'])
    # Payload zusammekriegen
    order_for_sns = {
        'id': order['id'],
        'items': products,
        'address': order['address']
    }

    client = boto3.client('lambda')
    arn = lambda_helper.get_arn('delivery-publish')
    sns_response = client.invoke(
        FunctionName=arn,
        InvocationType='RequestResponse',
        Payload=json.dumps(order_for_sns, cls=DecimalEncoder)
    )

    payload = sns_response['Payload']
    data = payload.read()
    response = Response(statusCode=sns_response['StatusCode'], body={"message": json.loads(data)})

    logging.warning(response.to_json())
    return response.to_json()


def get_products_for_sns(products):
    all_products_for_sns = []
    for product in products:
        sns_product = {
            'name': product['description'],
            'quantity': int(product['quantity'])
        }
        all_products_for_sns.append(sns_product)

    return all_products_for_sns
