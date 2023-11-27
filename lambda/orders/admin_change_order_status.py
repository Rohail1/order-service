import os
import json
import boto3
import datetime
from src.constants.status_codes import StatusCode, Messages
from src.constants.order_status import OrderStatus
from src.helpers.utils import send_response, normalize_dynamodb_values

ddb = boto3.resource('dynamodb')
order_table = ddb.Table(os.environ.get('ORDER_TABLE'))


def handler(event, context):
    try:
        print('request: {}'.format(json.dumps(event)))
        body = json.loads(event.get('body'))
        order_id = event.get('pathParameters').get('orderid')
        order = order_table.get_item(Key={"id": order_id})
        if 'Item' not in order:
            return send_response(status=StatusCode.HTTP_NOT_FOUND_404, message=Messages.NOT_FOUND)
        if body.get('status') is None or body.get('status') not in OrderStatus.STATUSES:
            return send_response(status=StatusCode.HTTP_BAD_REQUEST_400,
                                 message=Messages.BAD_REQUEST_INVALID_PARAMETER.format('status'))

        response = order_table.update_item(
            Key={'id': order_id},
            AttributeUpdates={
                'status': {
                    'Value': OrderStatus.get_status(body.get('status'))
                },
                'updated_at': {
                    'Value': datetime.datetime.now().isoformat()
                }
            },
            ReturnValues='ALL_NEW'
        )
        return send_response(data=normalize_dynamodb_values(response.get('Attributes')))
    except Exception as ex:
        return send_response(
            status=StatusCode.HTTP_INTERNAL_SERVER_ERROR_500, message=Messages.INTERNAL_SERVER_ERROR, data=str(ex))
