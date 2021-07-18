import urllib3
import json
import logging
from src.main.functions.helper import lambda_helper
from src.main.functions.helper.Response import Response
from src.main.functions.helper.decimalencoder import DecimalEncoder
from src.main.persistence import db_service
import boto3

table = db_service.get_orders_table()


def get_order(event, context):
    order_exists, order = db_service.does_item_exist(event['pathParameters']['id'], table)

    if order_exists:
        if order['status'] != 'pending' or order['invoice']:
            return return_existing_order(order)

        order_id = order['id']

        # Getting invoice pdf
        response_from_api = send_order_to_payment_api(order)
        order_from_api = json.loads(response_from_api.data)
        if order_from_api['status'] != 'accepted':
            response = Response(statusCode=400, body={'Message': 'The payment method was declined. Pleas try again '
                                                                 'with a valid credit card!'})
            set_status_and_invoice(order_id, 'declined', None)
            return response.to_json()

        logging.warning(order)
        set_status_and_invoice(order_id, 'accepted', order_from_api['invoice'])
        # Additionally changing order object to return to frontend
        order['status'] = 'accepted'
        order['invoice'] = order_from_api['invoice']

        # Getting delivery status and information
        response_from_sns = publish_to_sns_delivery(order)
        logging.warning(response_from_sns)

        response = Response(statusCode=200, body=order)
    else:
        response = Response(statusCode=404, body={'Message': 'Order not found!'})

    return response.to_json()


# Return response from payment api
def send_order_to_payment_api(order):
    payment_endpoint, header = lambda_helper.get_payment_api()
    http = urllib3.PoolManager()
    url = f"{payment_endpoint}/{order['id']}"
    return http.request('GET', url, headers=header, retries=True)


def publish_to_sns_delivery(order):
    products = get_products_for_sns(order['items'])
    # Payload zusammekriegen
    order_for_sns = {
        'id': order['id'],
        'items': products,
        'address': order['address']
    }

    logging.warning(order_for_sns)

    client = boto3.client('lambda')
    arn = lambda_helper.get_arn('delivery-publish')
    sns_response = client.invoke(
        FunctionName=arn,
        InvocationType='RequestResponse',
        Payload=json.dumps(order_for_sns, cls=DecimalEncoder)
    )

    if sns_response['StatusCode'] != 200:
        response = Response(statusCode=400, body={"message": "Error from SNS-topic. Please try again",
                                                  "Error": sns_response})
    else:
        response = Response(statusCode=200, body={"message": sns_response['Payload']})

    return response


def get_products_for_sns(products):
    all_products_for_sns = []
    for product in products:
        sns_product = {
            'name': product['description'],
            'quantity': int(product['quantity'])
        }
        all_products_for_sns.append(sns_product)

    return all_products_for_sns


def return_existing_order(order):
    if order['status'] == 'accepted':
        response = Response(statusCode=200, body=order)
    else:
        response = Response(statusCode=400, body={'Message': 'The payment method was declined. Pleas try again '
                                                             'with a valid credit card!'})
    return response.to_json()


def set_status_and_invoice(order_id, status, invoice):
    table.update_item(
        Key={
            'id': order_id
        },
        UpdateExpression='SET #st = :s, #in = :i',
        ExpressionAttributeValues={
            ":s": status,
            ":i": invoice,
        },
        ExpressionAttributeNames={
            "#st": "status",
            "#in": "invoice"
        }
    )
