import os
import datetime
import uuid
import json
import boto3
from src.constants.status_codes import StatusCode, Messages
from src.constants.order_status import OrderStatus
from src.helpers.utils import send_response, get_currency, get_product_price


ddb = boto3.resource('dynamodb')
user_email_table = ddb.Table(os.environ.get('USER_EMAIL_TABLE'))
order_table = ddb.Table(os.environ.get('ORDER_TABLE'))


def handler(event, context):
    try:
        print('request: {}'.format(json.dumps(event)))
        user_id = event.get('pathParameters').get('userid')
        body = json.loads(event.get('body'))
        products = body.get('products', [])

        if not products:
            return send_response(status=StatusCode.HTTP_BAD_REQUEST_400,
                                 message=Messages.BAD_REQUEST_INVALID_PARAMETER.format('products'))
        total = 0
        for product in products:
            if 'id' not in product or 'quantity' not in product:
                return send_response(status=StatusCode.HTTP_BAD_REQUEST_400,
                                     message=Messages.BAD_REQUEST_INVALID_PARAMETER.format('products'))
            product['price'] = get_product_price(product['id'])
            product['total'] = product['price'] * product['quantity']
            total += product['total']
        user_email = user_email_table.get_item(Key={"id": user_id})
        if 'Item' not in user_email:
            return send_response(status=StatusCode.HTTP_NOT_FOUND_404, message=Messages.NOT_FOUND)

        order_id = uuid.uuid4().hex
        order_object = {
            'id': order_id,
            'user_id': user_id,
            'products': products,
            'currency': get_currency(),
            'total': total,
            'status': OrderStatus.PENDING,
            'created_at': datetime.datetime.now().isoformat(),
            'updated_at': datetime.datetime.now().isoformat()
        }

        order_table.put_item(
            Item=order_object
        )

        return send_response(data=order_object)
    except Exception as ex:
        return send_response(
            status=StatusCode.HTTP_INTERNAL_SERVER_ERROR_500, message=Messages.INTERNAL_SERVER_ERROR, data=str(ex))
