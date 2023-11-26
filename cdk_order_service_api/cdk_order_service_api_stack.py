from aws_cdk import (
    Stack,
    aws_apigatewayv2_alpha as apigateway,
)
from constructs import Construct

from cdk_order_service_api.constructs.models import Models
from cdk_order_service_api.constructs.users import Users


class CdkOrderServiceApiStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Models
        models = Models(self, 'db-models')
        # Create an API Gateway
        api = apigateway.HttpApi(self, 'order-service')

        Users(self, 'user-apis', api=api, models=models)


