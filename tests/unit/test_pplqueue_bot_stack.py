import aws_cdk as core
import aws_cdk.assertions as assertions

from pplqueue_bot.pplqueue_bot_stack import PplqueueBotStack

# example tests. To run these tests, uncomment this file along with the example
# resource in pplqueue_bot/pplqueue_bot_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = PplqueueBotStack(app, "pplqueue-bot")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
