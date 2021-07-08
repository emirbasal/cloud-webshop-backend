import json
from src.functions.helper import decimalencoder
from src.functions.helper.Response import Response
from src.persistence import db_service


def get_order(event, context):
    table = db_service.get_orders_table()
    order_exists, order = db_service.does_item_exist(event, table)

    if order_exists:
        response = Response(statusCode=200, body=json.dumps(order, cls=decimalencoder.DecimalEncoder))
    else:
        response = Response(statusCode=404, body=json.dumps({'Message': 'Order not found'}))

    return response.to_json()
