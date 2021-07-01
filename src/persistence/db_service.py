import os

import boto3

dynamodb = boto3.resource('dynamodb')


def get_products_table():
    return dynamodb.Table(os.environ['PRODUCTS_TABLE'])


def get_orders_table():
    return dynamodb.Table(os.environ['ORDERS_TABLE'])


def does_item_exist(event, table):
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )

    # result is a dict
    if 'Item' in result:
        return True, result
    else:
        return False, result
