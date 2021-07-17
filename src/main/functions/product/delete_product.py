from src.main.functions.helper.Response import Response
from src.main.functions.helper.auth_helper import is_authenticated
from src.main.persistence import db_service


def delete_product(event, context):
    if is_authenticated(event):
        table = db_service.get_products_table()
        product_exists, item = db_service.does_item_exist(event['pathParameters']['id'], table)
        if product_exists:
            table.delete_item(
                Key={
                    'id': event['pathParameters']['id']
                }
            )
            response = Response(statusCode=200, body={'Message': 'Successfully deleted product.'})
        else:
            response = Response(statusCode=404, body={'Message': 'Product does not exists. Product not found'})
    else:
        response = Response(statusCode=403, body={'Message': 'Not authorized'})

    return response.to_json()
