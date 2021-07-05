import urllib3
import json
import logging
from src.functions import lambda_helper
from src.persistence import db_service


def get_invoice(event, context):
    table = db_service.get_orders_table()
    order_exists, order = db_service.does_item_exist(event, table)

    if order_exists:
        payment_endpoint, header = lambda_helper.get_payment_api()
        http = urllib3.PoolManager()
        order_id = order['id']

        url = f"{payment_endpoint}/{order_id}"
        response = http.request('GET', url, headers=header, retries=False)

        order = json.loads(response.data)
        if order['status'] != 'accepted':
            logging.error("There was an error creating this order. You have to order the items again!")

        table = db_service.get_orders_table()
        table.put_item(Item=order)
        logging.info(f'Order with ID {order["id"]} was updated!')

        response = {
            "statusCode": 200,
            "body": json.dumps(order)
        }
    else:
        response = {
            "statusCode": 406,
            "body": json.dumps({'Message': 'Order not found!'})
        }

    return response
