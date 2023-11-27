import json
import random
from src.constants.status_codes import StatusCode, Messages


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
