import json
import random
from src.constants.status_codes import StatusCode, Messages
from decimal import Decimal


def send_response(status=StatusCode.HTTP_OK_200, message=Messages.SUCCESSFUL, data=None, headers=None):
    if headers is None:
        headers = dict()
    _headers = {
        'Content-Type': 'text/json'
    }
    _headers.update(headers)
    return {
        'statusCode': status,
        'headers': _headers,
        'body': json.dumps({
            'message': message,
            'data': data
        })
    }


def get_currency():
    return 'USD'


def get_product_price(product_id):
    # Just a dummy function
    return random.randrange(1, 100)


def normalize_dynamodb_values(obj):
    if isinstance(obj, list):
        for i in range(len(obj)):
            obj[i] = normalize_dynamodb_values(obj[i])
        return obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            obj[k] = normalize_dynamodb_values(obj[k])
        return obj
    elif isinstance(obj, Decimal):
        if float(obj) % 1 == 0:
            return int(obj)
        return float(obj)
    else:
        return obj