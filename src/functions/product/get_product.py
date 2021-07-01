import json
from src.functions import decimalencoder
from src.persistence import db_service


def get_product(event, context):
    table = db_service.get_products_table()

    product_exists, result = does_product_exist(event, table)

    if product_exists:
        response = {
            "statusCode": 200,
            "body": json.dumps(result['Item'],
                               cls=decimalencoder.DecimalEncoder)
        }

    else:
        response = {
            "statusCode": 406,
            "body": json.dumps({'Message': 'Product not found'})
        }

    return response


def does_product_exist(event, table):
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
