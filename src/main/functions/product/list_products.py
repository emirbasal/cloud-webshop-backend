from src.main.helper.classes.response import Response
from src.main.helper.services import db_service


def list_products(event, context):
    table = db_service.get_products_table()
    result = table.scan()

    if 'Items' in result:
        response = Response(statusCode=200, body=result['Items'])
    else:
        response = Response(statusCode=404, body={'Message': 'Data not available.'})

    return response.to_json()
