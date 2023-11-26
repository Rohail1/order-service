import os
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
        user_id = event.get('pathParameters').get('userid')
        if body.get('first_name') is None or body.get('first_name') == '':
            return send_response(status=StatusCode.HTTP_BAD_REQUEST_400,
                                 message=Messages.BAD_REQUEST_INVALID_PARAMETER.format('first_name'))

        if body.get('last_name') is None or body.get('last_name') == '':
            return send_response(status=StatusCode.HTTP_BAD_REQUEST_400,
                                 message=Messages.BAD_REQUEST_INVALID_PARAMETER.format('last_name'))

        user_email = user_email_table.get_item(Key={"id": user_id})

        if 'Item' not in user_email:
            return send_response(status=StatusCode.HTTP_NOT_FOUND_404, message=Messages.NOT_FOUND)
        email = user_email.get('Item').get('email')

        response = user_table.update_item(
            Key={'email': email},
            AttributeUpdates={
                'first_name': {
                    'Value': body.get('first_name')
                },
                'last_name': {
                    'Value': body.get('last_name')
                }
            },
            ReturnValues='ALL_NEW'
        )
        print(response)
        return send_response(data=response.get('Attributes'))
    except Exception as ex:
        return send_response(
            status=StatusCode.HTTP_INTERNAL_SERVER_ERROR_500, message=Messages.INTERNAL_SERVER_ERROR, data=str(ex))
