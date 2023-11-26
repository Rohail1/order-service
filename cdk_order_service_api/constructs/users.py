from constructs import Construct
from aws_cdk import (
    aws_lambda as _lambda,
    aws_dynamodb as dynamodb,
    aws_logs as cwLogs,
    aws_apigatewayv2_alpha as apigateway,
    RemovalPolicy
)

from aws_cdk.aws_apigatewayv2_integrations_alpha import HttpLambdaIntegration
from cdk_order_service_api.constructs.models import Models


class Users(Construct):

    def __init__(self, scope: Construct, construct_id: str, api: apigateway.HttpApi, models=Models, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        dependency_layer = _lambda.LayerVersion(
            self, 'dependencies',
            code=_lambda.Code.from_asset('layers/'),
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_12],
            layer_version_name='dependencies'
        )

        create_user = _lambda.Function(
            self, 'create-user',
            runtime=_lambda.Runtime.PYTHON_3_12,
            code=_lambda.Code.from_asset('lambda/users'),
            handler='create_user.handler',
            layers=[dependency_layer],
            log_retention=cwLogs.RetentionDays.ONE_WEEK,
            environment={
                'USER_TABLE': models.user_table.table_name
            }

        )

        # Add integration between the API Gateway and the Lambda function
        integration = HttpLambdaIntegration('create-user-integration', create_user)

        # Add a default route to the API Gateway with the Lambda integration
        api.add_routes(
            path='/api/users',
            methods=[apigateway.HttpMethod.POST],
            integration=integration
        )

        models.user_table.grant_read_write_data(create_user)
