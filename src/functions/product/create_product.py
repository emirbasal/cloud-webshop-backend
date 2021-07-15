import json
import logging
import time
import uuid
from decimal import Decimal
from src.functions.helper.Response import Response
from src.persistence import db_service


# TODO: Input validation
def create_product(event, context):
    data = json.loads(event['body'])
    if 'name' not in data or 'description' not in data or 'currency' not in data or 'amount' not in data or \
            'image' not in data:
        logging.error("Validation Failed. Attribute(s) are missing. Couldn't create the product.")

        response = Response(statusCode=400, body={"message": "Validation Failed. Attribute(s) are missing. Couldn't "
                                                             "create the product."})

        return response.to_json()

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

    return response.to_json()
