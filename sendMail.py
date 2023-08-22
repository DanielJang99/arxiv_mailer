from __future__ import print_function
import httplib2
import os
from apiclient import discovery
from oauth2client import file, client, tools
import argparse
import base64
from email.mime.text import MIMEText
import sys
import boto3

flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
SCOPES = "https://mail.google.com/"
SECRET_FILE_PATH = os.environ["SECRET_FILE_PATH"]
BUCKET_NAME = os.environ["BUCKET_NAME"]
OBJECT_KEY = os.environ["SECRET_OBJECT_KEY"]
APPLICATION_NAME = "arxivMailer"


def get_credentials():
    """Gets valid user credentials from S3 storage.

    If the stored credentials are invalid, the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Obtained credential object.
    """
    s3 = boto3.client("s3")
    s3.download_file(BUCKET_NAME, OBJECT_KEY, SECRET_FILE_PATH)
    store = file.Storage(SECRET_FILE_PATH)
    try:
        credentials = store.get()
    except:
        flow = client.flow_from_clientsecrets(SECRET_FILE_PATH, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        s3.upload_file(SECRET_FILE_PATH, BUCKET_NAME, OBJECT_KEY)
    return credentials


def get_service():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build("gmail", "v1", http=http)
    return service


def create_message(sender, to, subject, message_text, style="html"):
    """Create a message for an email.

    Args:
      sender: Email address of the sender.
      to: Email address of the receiver.
      subject: The subject of the email message.
      message_text: The text of the email message.

    Returns:
      An object containing a base64url encoded email object.
    """
    message = MIMEText(message_text, _subtype=style)
    message["to"] = to
    message["from"] = sender
    message["subject"] = subject
    message = message.as_string()
    message = base64.urlsafe_b64encode(message.encode("utf-8")).decode("utf-8")
    return {"raw": message}


def send_message(message):
    """Send an email message.

    Args:
      message: Message to be sent.

    Returns:
      str: ID of the sent email message.
    """
    service = get_service()
    message = service.users().messages().send(userId="me", body=message).execute()
    return message["id"]
