import os

import boto3


def get_products_table():
    dynamodb = boto3.resource('dynamodb')
    return dynamodb.Table(os.environ['PRODUCTS_TABLE'])
