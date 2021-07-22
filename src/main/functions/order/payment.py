import json
import os
import uuid
import urllib3
from src.main.helper.services import external_resource_service, db_service
from src.main.helper.classes.response import Response


def payment(event, context):
    payment_endpoint, header = external_resource_service.get_payment_api()

    order_for_payment_api = create_order_for_payment_api(event)
    if not order_for_payment_api['items']:
        response = Response(statusCode=400, body={"message": "Product(s) can not be found in database"})
        return response.to_json()

    http = urllib3.PoolManager()
    response_from_payment_api = http.request('POST', payment_endpoint, body=json.dumps(order_for_payment_api),
                                             headers=header, retries=False)

    response = json.loads(response_from_payment_api.data)

    # Take status and invoice from payment api
    order_for_payment_api['status'] = response['status']
    order_for_payment_api['invoice'] = response['invoice']

    # Return this object bc it has more information which are needed then the response from the payment api
    return order_for_payment_api


def create_order_for_payment_api(order):
    order['id'] = str(uuid.uuid1())
    order['items'] = lookup_items(order['items'])
    order['amount'] = calc_amount(order['items'])
    order['currency'] = os.environ['SHOP_CURRENCY']
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
