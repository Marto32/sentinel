#! /usr/bin/env python
from flask import Flask
from flask_restful import Resource, Api, reqparse

from api_config import endpoints, push_objects
from contrib.api_utilities.instapush_api import SendNotification

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
        notifier = SendNotification(args['event_name'], args['trackers'])
        return notifier.emit()


class LogEvent(Resource):

    def post(self):
        # Define the requirements parser
        parser = reqparse.RequestParser()
        parser.add_argument('event_name', type=str, required=True, location='json')
        parser.add_argument('time', type=datetime, required=True, location='json')
        # TODO - add more based on what we want notification endpoint to do

        args = parser.parse_args(strict=True)
        # TODO - figure out how we want to log


# add endpoints using the config file
api.add_resource(NotifyUser, endpoints.get('notify'))
api.add_resource(LogEvent, endpoints.get('log'))


if __name__ == '__main__':

    # Set up logging
    # This obtains the log file using the LOGFILE environ variable
    # and the destination file name
    log_file = os.environ['LOGFILE'] + '/sentinel_api.log'
    logging_format = '[%(asctime)s] %(levelname)-s: %(message)s'
    handler = RotatingFileHandler(log_file, maxBytes=10485760, backupCount=20, encoding='utf8')
    handler.setLevel(logging.DEBUG)
    logging.basicConfig(format=logging_format, handlers=[handler])

    # Start the server
    app.run(debug=True)

