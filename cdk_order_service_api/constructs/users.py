from constructs import Construct
from aws_cdk import (
    aws_lambda as _lambda,
    aws_logs as cwLogs,
    aws_apigatewayv2_alpha as apigateway,
)

from aws_cdk.aws_apigatewayv2_integrations_alpha import HttpLambdaIntegration
from cdk_order_service_api.constructs.models import Models


class Users(Construct):

    def __init__(self, scope: Construct, construct_id: str, api: apigateway.HttpApi, models: Models,
                 dependency_layer: _lambda.LayerVersion, **kwargs) -> None:

        super().__init__(scope, construct_id, **kwargs)

        create_user = _lambda.Function(
            self, 'create-user',
            runtime=_lambda.Runtime.PYTHON_3_12,
            code=_lambda.Code.from_asset('lambda/users'),
            handler='create_user.handler',
            layers=[dependency_layer],
            log_retention=cwLogs.RetentionDays.ONE_WEEK,
            environment={
                'USER_TABLE': models.user_table.table_name,
                'USER_EMAIL_TABLE': models.user_email_table.table_name
            }

        )

        get_user = _lambda.Function(
            self, 'get-user',
            runtime=_lambda.Runtime.PYTHON_3_12,
            code=_lambda.Code.from_asset('lambda/users'),
            handler='get_user.handler',
            layers=[dependency_layer],
            log_retention=cwLogs.RetentionDays.ONE_WEEK,
            environment={
                'USER_TABLE': models.user_table.table_name,
                'USER_EMAIL_TABLE': models.user_email_table.table_name
            }

        )

        update_user = _lambda.Function(
            self, 'update-user',
            runtime=_lambda.Runtime.PYTHON_3_12,
            code=_lambda.Code.from_asset('lambda/users'),
            handler='update_user.handler',
            layers=[dependency_layer],
            log_retention=cwLogs.RetentionDays.ONE_WEEK,
            environment={
                'USER_TABLE': models.user_table.table_name,
                'USER_EMAIL_TABLE': models.user_email_table.table_name
            }

        )

        delete_user = _lambda.Function(
            self, 'delete-user',
            runtime=_lambda.Runtime.PYTHON_3_12,
            code=_lambda.Code.from_asset('lambda/users'),
            handler='delete_user.handler',
            layers=[dependency_layer],
            log_retention=cwLogs.RetentionDays.ONE_WEEK,
            environment={
                'USER_TABLE': models.user_table.table_name,
                'USER_EMAIL_TABLE': models.user_email_table.table_name
            }

        )

        # Add integration between the API Gateway and the Lambda function
        create_user_integration = HttpLambdaIntegration('create-user-integration', create_user)
        get_user_integration = HttpLambdaIntegration('get-user-integration', get_user)
        update_user_integration = HttpLambdaIntegration('update-user-integration', update_user)
        delete_user_integration = HttpLambdaIntegration('delete-user-integration', delete_user)

        # Add a default route to the API Gateway with the Lambda integration
        api.add_routes(
            path='/api/users',
            methods=[apigateway.HttpMethod.POST],
            integration=create_user_integration
        )
        api.add_routes(
            path='/api/users/{userid}',
            methods=[apigateway.HttpMethod.GET],
            integration=get_user_integration
        )

        api.add_routes(
            path='/api/users/{userid}',
            methods=[apigateway.HttpMethod.PUT],
            integration=update_user_integration
        )

        api.add_routes(
            path='/api/users/{userid}',
            methods=[apigateway.HttpMethod.DELETE],
            integration=delete_user_integration
        )

        # Grant Permission to table
        models.user_table.grant_read_write_data(create_user)
        models.user_email_table.grant_read_write_data(create_user)

        models.user_email_table.grant_read_data(get_user)
        models.user_table.grant_read_data(get_user)

        models.user_email_table.grant_read_data(update_user)
        models.user_table.grant_read_write_data(update_user)

        models.user_email_table.grant_read_write_data(delete_user)
        models.user_table.grant_read_write_data(delete_user)

