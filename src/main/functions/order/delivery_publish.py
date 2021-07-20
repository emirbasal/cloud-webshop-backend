import boto3
import logging
import os
import json
from src.main.helper.classes.response import Response


def delivery_publish(event, context):
    client = boto3.client('sns')

    # order = json.loads(event)
    logging.warning(event)
    sns_message = parse_order(event)
    response_sns = client.publish(
        TopicArn=os.environ['SNS_TOPIC_PUBLISH'],
        Message=json.dumps(sns_message)
    )

    logging.warning(response_sns)

    response = Response(statusCode=response_sns['ResponseMetadata']['HTTPStatusCode'], body=response_sns)

    return response.to_json()


def parse_order(order):
    products = get_products_for_sns(order['items'])
    # Payload zusammekriegen
    order_for_sns = {
        'id': order['id'],
        'items': products,
        'address': order['address']
    }
    return order_for_sns


def get_products_for_sns(products):
    all_products_for_sns = []
    for product in products:
        sns_product = {
            'name': product['description'],
            'quantity': int(product['quantity'])
        }
        all_products_for_sns.append(sns_product)

    return all_products_for_sns
