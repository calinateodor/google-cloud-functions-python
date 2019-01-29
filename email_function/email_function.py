import base64
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from oauth2client.client import GoogleCredentials
from httplib2 import Http


class SendEmail(object):
    def SendMessage(self, service, user_id, message):
        """Send an email message.

        Args:
          service: Authorized Gmail API service instance.
          user_id: User's email address. The special value "me"
          can be used to indicate the authenticated user.
          message: Message to be sent.

        Returns:
          Sent Message.
        """

        message = service.users().messages().send(userId=user_id, body=message).execute()
        return message

    def CreateMessage(self, sender, to, subject, message_text):
        """Create a message for an email.

        Args:
          sender: Email address of the sender.
          to: Email address of the receiver.
          subject: The subject of the email message.
          message_text: The text of the email message.

        Returns:
          An object containing a base64url encoded email object.
        """
        message = MIMEText(message_text)
        message['To'] = to
        message['From'] = sender
        message['Subject'] = subject

        return {"raw": base64.urlsafe_b64encode(message.as_bytes()).decode()}
