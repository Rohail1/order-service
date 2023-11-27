import os
import json
import boto3
from src.constants.status_codes import StatusCode, Messages
from src.helpers.utils import send_response

ddb = boto3.resource('dynamodb')
order_table = ddb.Table(os.environ.get('ORDER_TABLE'))


def handler(event, context):
    try:
        print('request: {}'.format(json.dumps(event)))
        order_id = event.get('pathParameters').get('orderid')
        order = order_table.get_item(Key={"id": order_id})
        if 'Item' not in order:
            return send_response(status=StatusCode.HTTP_NOT_FOUND_404, message=Messages.NOT_FOUND)
        order_table.delete_item(Key={"id": order_id})
        return send_response()
    except Exception as ex:
        return send_response(
            status=StatusCode.HTTP_INTERNAL_SERVER_ERROR_500, message=Messages.INTERNAL_SERVER_ERROR, data=str(ex))
