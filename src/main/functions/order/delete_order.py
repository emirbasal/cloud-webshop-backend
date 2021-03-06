from src.main.helper.classes.response import Response
from src.main.helper.services import db_service


def delete_order(event, context):
    table = db_service.get_orders_table()
    orders_exists, item = db_service.does_item_exist(event['pathParameters']['id'], table)

    if orders_exists:
        table.delete_item(
            Key={
                'id': event['pathParameters']['id']
            }
        )
        response = Response(statusCode=200, body={'Message': 'Successfully deleted order.'})
    else:
        response = Response(statusCode=404, body={'Message': 'Order does not exists. Order not found.'})

    return response.to_json()
