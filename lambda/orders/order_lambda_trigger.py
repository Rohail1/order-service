import os
import json
import boto3
from src.constants.status_codes import StatusCode, Messages
from src.helpers.utils import send_response

ddb = boto3.resource('dynamodb')
sns = boto3.client('sns')
order_table = ddb.Table(os.environ.get('ORDER_TABLE'))
topic_arn = os.environ.get('ORDER_TOPIC_ARN')


def handler(event, context):
    try:
        print('request: {}'.format(json.dumps(event)))
        records = event.get('Records')
        for record in records:
            created_at = record['dynamodb']['NewImage']['created_at']['S']
            order_id = record['dynamodb']['NewImage']['id']['S']
            total = record['dynamodb']['NewImage']['total']['N']
            if record.get('eventName') == 'INSERT':
                currency = record['dynamodb']['NewImage']['currency']['S']
                message = f'New order is created at {created_at}  with order id {order_id} and total amount {total} {currency}'
                sns.publish(Subject="New order is created", TopicArn=topic_arn, Message=message)
            elif record.get('eventName') == 'MODIFY':
                new_status = record['dynamodb']['NewImage']['status']['S']
                old_status = record['dynamodb']['OldImage']['status']['S']
                if not new_status == old_status:
                    message = f'Status of order with ID {order_id} has been changed to {new_status} from {old_status}'
                    sns.publish(Subject="Order status has been changed!", TopicArn=topic_arn, Message=message)
        return send_response()
    except Exception as ex:
        print(str(ex))
        return send_response(
            status=StatusCode.HTTP_INTERNAL_SERVER_ERROR_500, message=Messages.INTERNAL_SERVER_ERROR, data=str(ex))
