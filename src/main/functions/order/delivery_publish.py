import boto3
import logging
import os
import json
from src.main.functions.helper.Response import Response


def delivery_publish(event, context):
    client = boto3.client('sns')
    sns_message = json.dumps(event)
    response_sns = client.publish(
        TopicArn=os.environ['SNS_TOPIC_PUBLISH'],
        Message=sns_message
    )

    logging.warning(response_sns)

    response = Response(statusCode=response_sns['ResponseMetadata']['HTTPStatusCode'], body=response_sns)

    return response.to_json()
