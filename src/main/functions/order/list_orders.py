from src.main.functions.helper.Response import Response
from src.main.functions.helper.auth_helper import is_authenticated
from src.main.persistence import db_service


def list_orders(event, context):
    if is_authenticated(event):
        table = db_service.get_orders_table()
        result = table.scan()

        if 'Items' in result:
            response = Response(statusCode=200, body=result['Items'])
        else:
            response = Response(statusCode=404, body={'Message': 'Data not available.'})
    else:
        response = Response(statusCode=403, body={'Message': 'Not authorized'})

    return response.to_json()
