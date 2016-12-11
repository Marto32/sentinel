import requests
import simplejson
from api.util.api_helper import AbstractAPIHelper
from api.api_config import USER_TOKEN, APP_ID, APP_SECRET, push_objects


class AbstractSentinelInstapush(AbstractAPIHelper):

    user_token = USER_TOKEN
    app_name = push_objects.get('sentinel_app').get('app_name')
    app_id = APP_ID
    app_secret = APP_SECRET
    return_format = 'application/json'
    base_url = 'https://api.instapush.im/{version}/{endpoint}'
    api_version = 'v1'


class SendNotification(AbstractSentinelInstapush):
    """
    A POST request to instapush that will send a notification.
    NOTE: This should always be sent using this classes `emit` method.
    """

    endpoint = 'post'

    def __init__(self, event, trackers):
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
        self.event = event
        self.trackers = trackers

    @property
    def payload(self):
        params = {
            'event': self.event,
            'trackers': self.trackers
        }
        return simplejson.dumps(params)

    def build_request(self):
        headers = {
            'x-instapush-appid': self.app_id,
            'x-instapush-appsecret': self.app_secret,
            'Content-Type': self.return_format}

        url = self.base_url.format(endpoint=self.endpoint,
                                   version=self.api_version)
        return url, headers

    @property
    def execute_call(self):
        url, headers = self.build_request()
        return requests.post(
            url,
            headers=headers,
            data=self.payload)

    def parse_data(self, data):
        """
        Parses a Notification response object to return the message,
        error status and call status. Expects response format:

        {
            "msg": "Notification Sent Succesfully",
            "error": false,
            "status": 201
        }

        :param data: json, response object from an api call
        """
        message = data.get('msg')
        error = data.get('error')
        status = data.get('status')
        return message, error, status

    def emit(self):
        """
        Programmatically calls the following methods:

         * `execute_call`
         * `fetch_data`
         * `parse_data`

        :returns: message, error, status response tuple
        """
        return self.parse_data(self.fetch_data())
