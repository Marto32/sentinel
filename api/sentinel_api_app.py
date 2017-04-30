#! /usr/bin/env python
from flask import Flask, abort
from flask_restful import Resource, Api, reqparse

from api.api_config import endpoints, SENTINEL_SECRET_KEY
from api.contrib.twilio_api_helper import SendNotification
from api.util.logger_utility import get_logger

import os

from logging.handlers import RotatingFileHandler
import logging

from retrying import retry


# Define the app
app = Flask(__name__)
api = Api(app)


class NotifyUser(Resource):

    def post(self):
        # Define the requirements parser
        parser = reqparse.RequestParser()
        parser.add_argument('event_name', type=str, required=True, location='json')
        parser.add_argument('message', type=str, required=True, location='json')
        parser.add_argument('secretkey', type=str, required=True, location='headers')
        # TODO - add more based on what we want notification endpoint to do

        args = parser.parse_args(strict=True)
        if args['secretkey'] != SENTINEL_SECRET_KEY:
            abort(403)

        notifier = SendNotification(args['message'])
        notifier.emit()


class LogEvent(Resource):

    def post(self):
        # Define the requirements parser
        parser = reqparse.RequestParser()
        parser.add_argument('trigger_name', type=str, required=True, location='json')
        parser.add_argument('event_name', type=str, required=True, location='json')
        parser.add_argument('time', type=str, required=True, location='json')
        parser.add_argument('secretkey', type=str, required=True, location='headers')

        args = parser.parse_args(strict=True)
        if args['secretkey'] != SENTINEL_SECRET_KEY:
            abort(403)

        client_logger = get_logger('client')
        base_log_message = "{trigger_name}|{event_name}|{date_time}"
        client_logger.info(base_log_message.format(
            trigger_name=args['trigger_name'],
            event_name=args['event_name'],
            date_time=args['time']))


# add endpoints using the config file
api.add_resource(NotifyUser, endpoints.get('notify'))
api.add_resource(LogEvent, endpoints.get('log'))


@retry(stop_max_attempt_number=30, wait_fixed=500)
def main():
    """
    Launch the server and retry if an exception is thrown
    in app.run. Set max retries at 30, wait .5 seconds between
    each try.
    """
    app.run(host='0.0.0.0', debug=True, port=8080)

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
    main()
