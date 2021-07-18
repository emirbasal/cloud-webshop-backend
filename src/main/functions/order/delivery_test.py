import boto3
import logging
import os
import json
from src.main.functions.helper.Response import Response


def delivery_publish(event, context):
    client = boto3.client('sns')

    message = {
        "id": "42f8f1b2-16ae-40aa-aaa6-34660564A222",
        "items": [{
            "name": "Foo-Ding",
            "quantity": 66
        }, {
            "name": "Bar-Widget",
            "quantity": 6
        }],
        "address": {
            "country": "Japan",
            "state": "",
            "city": "Testcity",
            "zip": "44444444",
            "address1": "Max Mustermann",
            "address2": "Teststr. 19",
            "address3": ""
        }
    }

    response_sns = client.publish(
        TopicArn= os.environ['SNS_TOPIC_PUBLISH'],
        Message=json.dumps(message)
    )

    response = Response(statusCode=200, body=response_sns)
    logging.warning(response.to_json())

    return response.to_json()
