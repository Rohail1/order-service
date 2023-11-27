from aws_cdk import (
    Stack,
    aws_apigatewayv2_alpha as apigateway,
    aws_lambda as _lambda
)
from constructs import Construct

from cdk_order_service_api.constructs.models import Models
from cdk_order_service_api.constructs.users import Users
from cdk_order_service_api.constructs.orders import Orders


class CdkOrderServiceApiStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Models
        models = Models(self, 'db-models')
        # Create an API Gateway
        api = apigateway.HttpApi(self, 'order-service')

        # Layers

        dependency_layer = _lambda.LayerVersion(
            self, 'dependencies',
            code=_lambda.Code.from_asset('layers/'),
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_12],
            layer_version_name='dependencies'
        )

        Users(self, 'user-apis', api=api, models=models, dependency_layer=dependency_layer)

        Orders(self, 'order-apis', api=api, models=models, dependency_layer=dependency_layer)
