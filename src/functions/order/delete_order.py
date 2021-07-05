import json
from src.persistence import db_service


def delete_order(event, context):
    table = db_service.get_orders_table()

    orders_exists, item = db_service.does_item_exist(event, table)

    if orders_exists:
        table.delete_item(
            Key={
                'id': event['pathParameters']['id']
            }
        )
        response = {
            "statusCode": 200,
            "body": json.dumps({'Message': 'Successfully deleted order.'})
        }
    else:
        response = {
            "statusCode": 406,
            "body": json.dumps({'Message': 'Order does not exists. Order not found.'})
        }

    return response
