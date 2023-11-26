import os
import re
import uuid
import json
import boto3
from src.constants.status_codes import StatusCode, Messages
from src.helpers.utils import send_response

ddb = boto3.resource('dynamodb')
user_table = ddb.Table(os.environ.get('USER_TABLE'))
user_email_table = ddb.Table(os.environ.get('USER_EMAIL_TABLE'))
_lambda = boto3.client('lambda')


def handler(event, context):
    try:
        print('request: {}'.format(json.dumps(event)))
        body = json.loads(event.get('body'))

        if body.get('first_name') is None or body.get('first_name') == '':
            return send_response(status=StatusCode.HTTP_BAD_REQUEST_400,
                                 message=Messages.BAD_REQUEST_INVALID_PARAMETER.format('first_name'))

        if body.get('last_name') is None or body.get('last_name') == '':
            return send_response(status=StatusCode.HTTP_BAD_REQUEST_400,
                                 message=Messages.BAD_REQUEST_INVALID_PARAMETER.format('last_name'))

        if body.get('email') is None or body.get('email') == '' or not re.match(r"[^@]+@[^@]+\.[^@]+",
                                                                                body.get('email')):
            return send_response(status=StatusCode.HTTP_BAD_REQUEST_400,
                                 message=Messages.BAD_REQUEST_INVALID_PARAMETER.format('email'))

        user_id = uuid.uuid4().hex
        email = body.get('email').lower().strip()
        user_data = {
            'id': user_id,
            'first_name': str(body.get('first_name')),
            'last_name': str(body.get('last_name')),
            'email': email
        }

        user_email_data = {
            'id': user_id,
            'email': email
        }

        user = user_table.get_item(Key={"email": body.get('email')})
        if 'Item' in user:
            return send_response(status=StatusCode.HTTP_BAD_REQUEST_400, message=Messages.BAD_REQUEST_EMAIL_EXIST)

        user_table.put_item(
            Item=user_data
        )
        user_email_table.put_item(
            Item=user_email_data
        )
        return send_response(data=user_data)
    except Exception as ex:
        return send_response(
            status=StatusCode.HTTP_INTERNAL_SERVER_ERROR_500, message=Messages.INTERNAL_SERVER_ERROR, data=str(ex))
