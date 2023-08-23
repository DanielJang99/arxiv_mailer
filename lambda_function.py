import json
from arxiv_feeder import main
from personal_variables import sender_mail_address, receiver_mail_address


def lambda_handler(event, context):
    """Evokes email notification through AWS Lambda"""
    main()
    return {"statusCode": 200}
