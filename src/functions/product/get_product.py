from src.functions.helper.Response import Response
from src.persistence import db_service


def get_product(event, context):
    table = db_service.get_products_table()

    product_exists, result = db_service.does_item_exist(event, table)

    if product_exists:
        response = Response(statusCode=200, body=result)
    else:
        response = Response(statusCode=404, body={'Message': 'Product not found'})

    return response.to_json()
