"""
This module will be used to interface with the Instapush API to send
push notifications to the end user. It uses another module's api
helper as its base class. That other module (instapush_api)
is not currently in this repo.
"""
from contrib.api_utilities.instapush_api import SendNotification
from util.constants import INSTAPUSH_SENTINEL_APPLICATION_SECRET, INSTAPUSH_SENTINEL_APPLICATION_ID
from api.api_config import push_objects


class SentinelNotification(SendNotification):

    @property
    def app_name(self):
        return push_objects.get('sentinel_app').get('app_name')

    @property
    def app_id(self):
        return INSTAPUSH_SENTINEL_APPLICATION_ID

    @property
    def app_secret(self):
        return INSTAPUSH_SENTINEL_APPLICATION_SECRET

