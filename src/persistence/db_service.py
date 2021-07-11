import os

import boto3


dynamodb = boto3.resource('dynamodb')


# TODO: REMOVE
def get_products_table():
    return dynamodb.Table(os.environ['PRODUCTS_TABLE'])


# TODO: REMOVE
def get_orders_table():
    return dynamodb.Table(os.environ['ORDERS_TABLE'])


def get_table(table_name):
    return dynamodb.Table(os.environ[table_name])


def does_item_exist(item_id, table):
    result = table.get_item(
        Key={
            'id': item_id
        }
    )

    # result is a dict
    if 'Item' in result:
        return True, result['Item']
    else:
        return False, result


def does_user_exist(username, table):
    result = table.get_item(
        Key={
            'username': username
        }
    )
    # result is a dict
    if 'Item' in result:
        return True, result['Item']
    else:
        return False, result

