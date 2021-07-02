import os


def get_arn(function_name):
    region = os.environ['REGION']
    account_id = os.environ['ACCOUNT_ID']
    stage = os.environ['STAGE']
    service = os.environ['SERVICE']

    return f'arn:aws:lambda:{region}:{account_id}:function:{service}-{stage}-{function_name}'
