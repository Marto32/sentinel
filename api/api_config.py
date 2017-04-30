"""
This module should house all of the configurations needed for the API.
For example, all endpoints, credentials, etc.
"""
import os

# Set an endpoint dictionary which will be used by the API
endpoints = {
        'notify': '/sentinel/v1/notify',
        'log'   : '/sentinel/v1/log'
        }

# Sentinel secret key
SENTINEL_SECRET_KEY = os.environ.get('SENTINEL_SECRET_KEY')

# Twilio Credentials
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
# Phone numbers must be in the format +1xxxxxxxxxx
TWILIO_SOURCE_PHONE = os.environ.get('TWILIO_SOURCE_PHONE')
TWILIO_DESTINATION_PHONE =os.environ.get('TWILIO_DESTINATION_PHONE')
