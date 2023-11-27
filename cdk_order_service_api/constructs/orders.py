from constructs import Construct
from aws_cdk import (
    aws_lambda as _lambda,
    aws_logs as cwLogs,
    aws_apigatewayv2_alpha as apigateway,
)

from aws_cdk.aws_apigatewayv2_integrations_alpha import HttpLambdaIntegration
from cdk_order_service_api.constructs.models import Models


class Orders(Construct):

    def __init__(self, scope: Construct, construct_id: str, api: apigateway.HttpApi, models: Models,
                 dependency_layer: _lambda.LayerVersion,  **kwargs) -> None:

        super().__init__(scope, construct_id, **kwargs)

        create_user_order = _lambda.Function(
            self, 'create-order',
            runtime=_lambda.Runtime.PYTHON_3_12,
            code=_lambda.Code.from_asset('lambda/orders'),
            handler='create_order.handler',
            layers=[dependency_layer],
            log_retention=cwLogs.RetentionDays.ONE_WEEK,
            environment={
                'USER_EMAIL_TABLE': models.user_email_table.table_name,
                'ORDER_TABLE': models.order_table.table_name
            }

        )

        get_user_orders = _lambda.Function(
            self, 'get-user-orders',
            runtime=_lambda.Runtime.PYTHON_3_12,
            code=_lambda.Code.from_asset('lambda/orders'),
            handler='get_user_orders.handler',
            layers=[dependency_layer],
            log_retention=cwLogs.RetentionDays.ONE_WEEK,
            environment={
                'USER_EMAIL_TABLE': models.user_email_table.table_name,
                'ORDER_TABLE': models.order_table.table_name
            }

        )

        create_order_integration = HttpLambdaIntegration('create-order-integration', create_user_order)
        get_user_orders_integration = HttpLambdaIntegration('get-user-orders-integration', get_user_orders)

        api.add_routes(
            path='/api/users/{userid}/orders',
            methods=[apigateway.HttpMethod.POST],
            integration=create_order_integration
        )
        api.add_routes(
            path='/api/users/{userid}/orders',
            methods=[apigateway.HttpMethod.GET],
            integration=get_user_orders_integration
        )

        # Grant Permission to table
        models.user_email_table.grant_read_data(create_user_order)
        models.order_table.grant_read_write_data(create_user_order)

        models.user_email_table.grant_read_data(get_user_orders)
        models.order_table.grant_read_data(get_user_orders)
