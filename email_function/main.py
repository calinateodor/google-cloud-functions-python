import base64
from email.mime.text import MIMEText
from email_function import SendEmail
from googleapiclient.discovery import build
from oauth2client.client import GoogleCredentials
from httplib2 import Http


def send_email(data, context):
    """Background Cloud Function to be triggered by Pub/Sub.
    Args:
         data (dict): The dictionary with data specific to this type of event.
         context (google.cloud.functions.Context): The Cloud Functions event
         metadata.
    """

    sender = 'sender@email.com' # Add sender address here. Google service accounts cannot send emails, the sender email will be used instead. Only works if the service account has domain wide access.
    to = 'email@email.com' # Add email address here
    subject = 'It works'
    SCOPES = 'https://mail.google.com/'

    credentials = GoogleCredentials.get_application_default()
    credentials = credentials.create_scoped([SCOPES])

    http = credentials.authorize(Http.Http())
    service = build('gmail', 'v1', http=http)

    send_emails = SendEmail()
    if 'data' in data:
        message_text = "lets see if this works"
        message = send_emails.CreateMessage(sender=sender, to=to, subject=subject, message_text=message_text)
        send_emails.SendMessage(service, 'me', message)
