"""
This module will be used to interface with the Instapush API to send
push notifications to the end user. It uses another module's api
helper as its base class. That other module (instapush_api)
is not currently in this repo.
"""
from api.contrib.instapush_api import SendNotification
from api.api_config import push_objects, APP_ID, APP_SECRET


class SentinelNotification(SendNotification):

    @property
    def app_name(self):
        return push_objects.get('sentinel_app').get('app_name')

    @property
    def app_id(self):
        return APP_ID

    @property
    def app_secret(self):
        return APP_SECRET

