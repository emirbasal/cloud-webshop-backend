import urllib3
import json
import boto3
from src.main.helper.services import external_resource_service, db_service
from src.main.helper.classes.response import Response
from src.main.helper.classes.decimalencoder import DecimalEncoder

table = db_service.get_orders_table()


def get_order(event, context):
    order_exists, order = db_service.does_item_exist(event['pathParameters']['id'], table)

    if order_exists:
        if order['status'] == 'declined':
            response = Response(statusCode=400, body={'Message': 'The payment method was declined. Pleas try again '
                                                                 'with a valid credit card!'})

        elif order['status'] == 'accepted' and order['invoice']:
            response = Response(statusCode=200, body=order)

            # Checking if informations for delivery is already existent. If yes publish infos to delivery sns topic
            if 'deliveryStatus' not in order or not order['deliveryStatus']:
                publish_to_sns_delivery(order)

        else:
            # Status is pending

            # Getting invoice pdf from payment api
            response_from_api = send_order_to_payment_api(order)
            order_from_api = json.loads(response_from_api.data)

            set_status_and_invoice(order_from_api['id'], order_from_api['status'], order_from_api['invoice'])

            # Additionally changing order object to return to frontend
            order['status'] = order_from_api['status']
            order['invoice'] = order_from_api['invoice']

            if order_from_api['status'] == 'declined':
                response = Response(statusCode=400, body=order)
            else:
                response = Response(statusCode=200, body=order)

    else:
        response = Response(statusCode=404, body={'Message': 'Order not found!'})

    return response.to_json()


# Returns response from payment api
def send_order_to_payment_api(order):
    payment_endpoint, header = external_resource_service.get_payment_api()
    http = urllib3.PoolManager()
    url = f"{payment_endpoint}/{order['id']}"
    return http.request('GET', url, headers=header, retries=True)


# Update entry in order table
def set_status_and_invoice(order_id, status, invoice):
    table.update_item(
        Key={
            'id': order_id
        },
        UpdateExpression='SET #st = :s, #in = :i',
        ExpressionAttributeValues={
            ":s": status,
            ":i": invoice,
        },
        ExpressionAttributeNames={
            "#st": "status",
            "#in": "invoice"
        }
    )


def publish_to_sns_delivery(order):
    client = boto3.client('lambda')
    arn = external_resource_service.get_arn('delivery-publish')
    sns_response = client.invoke(
        FunctionName=arn,
        InvocationType='RequestResponse',
        Payload=json.dumps(order, cls=DecimalEncoder)
    )

    payload = sns_response['Payload']
    data = payload.read()
    response = Response(statusCode=sns_response['StatusCode'], body={"message": json.loads(data)})

    return response.to_json()
