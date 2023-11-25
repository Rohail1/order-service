import aws_cdk as core
import aws_cdk.assertions as assertions

from cdk_order_service_api.cdk_order_service_api_stack import CdkOrderServiceApiStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cdk_order_service_api/cdk_order_service_api_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CdkOrderServiceApiStack(app, "cdk-order-service-api")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
