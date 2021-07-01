import json
from src.functions import decimalencoder
from src.persistence import db_service


def list_orders(event, context):
    table = db_service.get_orders_table()

    result = table.scan()

    if 'Items' in result:
        response = {
            "statusCode": 200,
            "body": json.dumps(result['Items'], cls=decimalencoder.DecimalEncoder)
        }
    else:
        response = {
            "statusCode": 404,
            "body": json.dumps({'Message': 'Data not available.'})
        }

    return response
