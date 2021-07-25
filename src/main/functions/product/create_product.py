import json
import time
import uuid
from src.main.helper.classes.response import Response
from src.main.helper.services.auth_service import is_authenticated
from src.main.helper.services import db_service


def create_product(event, context):
    if is_authenticated(event):
        data = json.loads(event['body'])
        if not is_data_valid(data):
            response = Response(statusCode=400, body={"message": "Validation Failed. Attribute(s) are "
                                                                 "missing. Couldn't create the product."})

        else:
            timestamp = str(time.time())
            item = {
                'id': str(uuid.uuid1()),
                'name': data['name'],
                'description': data['description'],
                'amount': data['amount'],
                'currency': data['currency'],
                'image': data['image'],
                'createdAt': timestamp,
                'updatedAt': timestamp,
            }
            table = db_service.get_products_table()
            table.put_item(Item=item)
            response = Response(statusCode=200, body=item)
    else:
        response = Response(statusCode=403, body={'Message': 'Not authorized'})

    return response.to_json()


def is_data_valid(data):
    if 'name' in data and 'description' in data and 'currency' in data and 'amount' in data and 'image' and data:
        if data['name'] and data['description'] and data['currency'] and data['amount'] and data['image']:
            return True
    return False
