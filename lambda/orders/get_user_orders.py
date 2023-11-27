import os
import json
import boto3
from src.constants.status_codes import StatusCode, Messages
from src.helpers.utils import send_response, normalize_dynamodb_values

ddb = boto3.resource('dynamodb')
user_email_table = ddb.Table(os.environ.get('USER_EMAIL_TABLE'))
order_table = ddb.Table(os.environ.get('ORDER_TABLE'))


def handler(event, context):
    try:
        print('request: {}'.format(json.dumps(event)))
        user_id = event.get('pathParameters').get('userid')
        user_email = user_email_table.get_item(Key={"id": user_id})
        if 'Item' not in user_email:
            return send_response(status=StatusCode.HTTP_NOT_FOUND_404, message=Messages.NOT_FOUND)
        orders = order_table.query(
            IndexName='user_id',
            KeyConditionExpression="user_id = :userid",
            ExpressionAttributeValues={':userid': user_id}
        )
        return send_response(data=normalize_dynamodb_values(orders.get('Items')))
    except Exception as ex:
        return send_response(
            status=StatusCode.HTTP_INTERNAL_SERVER_ERROR_500, message=Messages.INTERNAL_SERVER_ERROR, data=str(ex))
