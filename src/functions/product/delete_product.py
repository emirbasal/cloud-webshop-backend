import json

from src.functions.helper.Response import Response
from src.persistence import db_service


def delete_product(event, context):
    table = db_service.get_products_table()

    product_exists, item = db_service.does_item_exist(event, table)

    if product_exists:
        table.delete_item(
            Key={
                'id': event['pathParameters']['id']
            }
        )

        response = Response(statusCode=200, body=json.dumps({'Message': 'Successfully deleted product.'}))
    else:
        response = Response(statusCode=404, body=json.dumps({'Message': 'Product does not exists. Product not found'}))

    return response.to_json()
