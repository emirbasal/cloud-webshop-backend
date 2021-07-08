import os


def get_arn(function_name):
    region = os.environ['REGION']
    account_id = os.environ['ACCOUNT_ID']
    stage = os.environ['STAGE']
    service = os.environ['SERVICE']

    return f'arn:aws:lambda:{region}:{account_id}:function:{service}-{stage}-{function_name}'


def get_payment_api():
    payment_endpoint = os.environ['PAYMENT_API']
    api_key = os.environ['PAYMENT_API_KEY']
    headers = {'Content-type': 'application/json', 'api_key': api_key}

    return payment_endpoint, headers


def get_response_header():
    return {"Access-Control-Allow-Origin": "*"}
