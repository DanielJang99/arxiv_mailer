import json
from arxiv_feeder import main
from personal_variables import sender_mail_address, receiver_mail_address


def lambda_handler(event, context):
    """Evokes email notification through AWS Lambda"""
    message_ids = main()
    return {"statusCode": 200, "message_ids": message_ids}
