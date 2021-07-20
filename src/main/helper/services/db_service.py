import os
import boto3
from botocore.client import Config


AWS_CONFIG = Config(region_name=os.environ['REGION'], retries={'max_attempts': 100})
dynamodb = boto3.resource('dynamodb', config=AWS_CONFIG)


def get_products_table():
    return dynamodb.Table(os.environ['PRODUCTS_TABLE'])


def get_orders_table():
    return dynamodb.Table(os.environ['ORDERS_TABLE'])


def get_users_table():
    return dynamodb.Table(os.environ['USERS_TABLE'])


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
