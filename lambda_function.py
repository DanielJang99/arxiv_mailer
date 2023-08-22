import json
from arxiv_feeder import send_todays_arxiv
from personal_variables import sender_mail_address, receiver_mail_address


def lambda_handler(event, context):
    """Evokes email notification through AWS Lambda"""
    msg_ids = send_todays_arxiv(sender=sender_mail_address, to=receiver_mail_address)
    return {"statusCode": 200, "body": json.dumps(msg_ids)}
