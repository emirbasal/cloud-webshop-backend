import json
from src.functions.helper import decimalencoder
from src.persistence import db_service


def get_order(event, context):
    table = db_service.get_orders_table()

    order_exists, order = db_service.does_item_exist(event, table)

    if order_exists:
        response = {
            "statusCode": 200,
            "body": json.dumps(order,
                               cls=decimalencoder.DecimalEncoder)
        }
    else:
        response = {
            "statusCode": 406,
            "body": json.dumps({'Message': 'Order not found'})
        }

    return response
