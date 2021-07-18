import os
import logging
import json

from src.main.persistence import db_service


table = db_service.get_orders_table()


def save_status_to_order(event, context):
    message = json.loads(event['Records'][0]['Sns']['Message'])
    logging.warning(message)

    order_id_from_sns = message.pop('id')
    all_orders = table.scan()

    for order in all_orders['Items']:
        if order_id_from_sns == order['id'] and order['status'] == 'accepted':
            set_delivery_status(order_id_from_sns, message)
    # {
    #     "id": "c8843f38-e7cd-11eb-80c3-cf793be3c581",
    #     "status": "sent",
    #     "comment": "I've sent: * 1 Foo-Dings\n* 2 Bar-Widgets\n\nto:\naf\nads\nasd\n234 asd\n\nsad\nsad\nDie Post freut sich...\n"
    # }


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
            "#st": "delivery_status"
        }
    )