import json
from src.main.helper.services import db_service

table = db_service.get_orders_table()


# Gets triggered by sns topic
def save_status_to_order(event, context):
    message = json.loads(event['Records'][0]['Sns']['Message'])

    order_id_from_sns = message.pop('id')
    all_orders = table.scan()

    for order in all_orders['Items']:
        if order_id_from_sns == order['id'] and order['status'] == 'accepted':
            set_delivery_status(order_id_from_sns, message)


# Updates order entry
def set_delivery_status(order_id, status):
    table.update_item(
        Key={
            'id': order_id
        },
        UpdateExpression='SET #st = :s',
        ExpressionAttributeValues={
            ":s": status
        },
        ExpressionAttributeNames={
            "#st": "deliveryStatus"
        }
    )
