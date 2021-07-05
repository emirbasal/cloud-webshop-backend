import json
from src.functions import decimalencoder
from src.persistence import db_service


def get_product(event, context):
    table = db_service.get_products_table()

    product_exists, result = db_service.does_item_exist(event, table)

    if product_exists:
        response = {
            "statusCode": 200,
            "body": json.dumps(result,
                               cls=decimalencoder.DecimalEncoder)
        }

    else:
        response = {
            "statusCode": 406,
            "body": json.dumps({'Message': 'Product not found'})
        }

    return response
