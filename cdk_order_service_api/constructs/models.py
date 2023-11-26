from constructs import Construct
from aws_cdk import (
    aws_dynamodb as dynamodb,
    RemovalPolicy
)


class Models(Construct):


    @property
    def user_table(self) -> dynamodb.Table:
        return self._users

    @property
    def user_email_table(self) -> dynamodb.Table:
        return self._emails

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self._emails = dynamodb.Table(
            self, 'users-emails',
            partition_key={
                'name': 'id', 'type': dynamodb.AttributeType.STRING
            },
            removal_policy=RemovalPolicy.DESTROY
           )

        self._users = dynamodb.Table(
            self, 'users',
            partition_key={
                'name': 'email', 'type': dynamodb.AttributeType.STRING
            },
            removal_policy=RemovalPolicy.DESTROY
           )

