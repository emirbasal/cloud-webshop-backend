import urllib3
import json
import logging
from src.functions.helper import lambda_helper
from src.functions.helper.Response import Response
from src.persistence import db_service


table = db_service.get_orders_table()


def get_invoice(event, context):
    order_exists, order = db_service.does_item_exist(event, table)

    if order_exists:
        payment_endpoint, header = lambda_helper.get_payment_api()
        http = urllib3.PoolManager()
        order_id = order['id']

        url = f"{payment_endpoint}/{order_id}"
        response = http.request('GET', url, headers=header, retries=False)
        logging.warning(response.data)

        order = json.loads(response.data)
        if order['status'] != 'accepted':
            response = Response(statusCode=400, body={'Message': 'The payment method was declined. Pleas try again '
                                                                 'with a valid credit card!'})

            set_status_and_invoice(order_id, 'declined', None)

            return response.to_json()

        set_status_and_invoice(order_id, 'accepted', order["invoice"])

        response = Response(statusCode=200, body=order)
    else:
        response = Response(statusCode=404, body={'Message': 'Order not found!'})

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
