import json
from src.functions.helper import decimalencoder, lambda_helper
from src.functions.helper.Response import Response
from src.persistence import db_service


def list_products(event, context):
    table = db_service.get_products_table()
    result = table.scan()

    if 'Items' in result:
        response = Response(statusCode=200, body=json.dumps(result['Items'], cls=decimalencoder.DecimalEncoder))
    else:
        response = Response(statusCode=404, body=json.dumps({'Message': 'Data not available.'}))

    return response.to_json()
