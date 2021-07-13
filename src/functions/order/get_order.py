from src.functions.helper.Response import Response
from src.persistence import db_service


def get_order(event, context):
    table = db_service.get_orders_table()
    order_exists, order = db_service.does_item_exist(event['pathParameters']['id'], table)

    if order_exists:
        response = Response(statusCode=200, body=order)
    else:
        response = Response(statusCode=404, body={'Message': 'Order not found'})

    return response.to_json()
