from twilio.rest import Client
from settings import (
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    TWILIO_SOURCE_PHONE,
    TWILIO_DESTINATION_PHONE
)


class SendNotification(object):
    """
    A POST request to twilio that will send a notification.
    NOTE: This should always be sent using this classes `emit` method.
    """

    def __init__(self, message: str) -> None:
        # TODO(Doc): Update Docstring
        """
        :param event: string, event name
        :param trackers: dict, params you use in the event with their values

        These will eventually be parsed for the request. For example:

        {
            "event": "signups",
            "trackers": {
                "email": "myemail"
            }
        }
        """
        self.message_body = message
        self.client = Client(
            TWILIO_ACCOUNT_SID,
            TWILIO_AUTH_TOKEN
        )

    @property
    def payload(self) -> dict:
        params = {
            'body': self.message_body,
            'to': TWILIO_DESTINATION_PHONE,
            'from_': TWILIO_SOURCE_PHONE,
        }
        return params

    def emit(self) -> Client.messages.create:
        """
        Calls twilio with the specified payload
        """
        return self.client.messages.create(
            **self.payload
        )

