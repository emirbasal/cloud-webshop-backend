import json
import logging
import time
import uuid
from src.main.helper.classes.response import Response
from src.main.helper.services.auth_service import is_authenticated
from src.main.helper.services import db_service


def create_product(event, context):
    if is_authenticated(event):
        data = json.loads(event['body'])
        if 'name' not in data or 'description' not in data or 'currency' not in data or 'amount' not in data or \
                'image' not in data:

            response = Response(statusCode=400, body={"message": "Validation Failed. Attribute(s) are "
                                                                 "missing. Couldn't create the product."})

        else:
            timestamp = str(time.time())
            table = db_service.get_products_table()

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
            table.put_item(Item=item)
            response = Response(statusCode=200, body=item)

            logging.warning(f'Produkt {item["id"]} wurde angelegt')
    else:
        response = Response(statusCode=403, body={'Message': 'Not authorized'})

    return response.to_json()
