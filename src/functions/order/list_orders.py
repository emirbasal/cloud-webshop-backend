from src.functions.helper.Response import Response
from src.persistence import db_service


def list_orders(event, context):
    table = db_service.get_orders_table()
    result = table.scan()

    if 'Items' in result:
        response = Response(statusCode=200, body=result['Items'])
    else:
        response = Response(statusCode=404, body={'Message': 'Data not available.'})

    return response.to_json()
