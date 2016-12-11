#! /usr/bin/env python
from flask import Flask
from flask_restful import Resource, Api, reqparse

from api.api_config import endpoints, push_objects
from api.contrib.notify_api import SentinelNotification
from api.util.logger_utility import get_logger

from datetime import datetime
import simplejson
import os

from logging.handlers import RotatingFileHandler
import logging


# Define the app
app = Flask(__name__)
api = Api(app)


class NotifyUser(Resource):

    notifications = push_objects.get('sentinel_app')

    def get(self):
        return notifications

    def post(self):
        # Define the requirements parser
        parser = reqparse.RequestParser()
        parser.add_argument('event_name', type=str, required=True, location='json')
        parser.add_argument('trackers', type=dict, required=True, location='json')
        # TODO - add more based on what we want notification endpoint to do

        args = parser.parse_args(strict=True)

        notify_events = push_objects.get('sentinel_app').get('events')
        notifier = SentinelNotification(notify_events.get(
            args['event_name']), args['trackers'])
        notifier.emit()


class LogEvent(Resource):

    def post(self):
        # Define the requirements parser
        parser = reqparse.RequestParser()
        parser.add_argument('trigger_name', type=str, required=True, location='json')
        parser.add_argument('event_name', type=str, required=True, location='json')
        parser.add_argument('time', type=str, required=True, location='json')

        args = parser.parse_args(strict=True)
        client_logger = get_logger('client')

        base_log_message = "{trigger_name}|{event_name}|{date_time}"
        client_logger.info(base_log_message.format(
            trigger_name=args['trigger_name'],
            event_name=args['event_name'],
            date_time=args['time']))


# add endpoints using the config file
api.add_resource(NotifyUser, endpoints.get('notify'))
api.add_resource(LogEvent, endpoints.get('log'))


if __name__ == '__main__':
    # Set up logging so we keep track of all server messages
    # This obtains the log file using the LOGFILE environ variable
    # and the destination file name
    log_file = os.environ['LOGFILE'] + '/sentinel_api.log'
    logging_format = '[%(asctime)s] %(levelname)-s: %(message)s'
    handler = RotatingFileHandler(log_file, maxBytes=10485760, backupCount=20, encoding='utf8')
    handler.setLevel(logging.DEBUG)
    logging.basicConfig(format=logging_format, handlers=[handler], level=logging.DEBUG)

    # Start the server
    app.run(debug=True)

