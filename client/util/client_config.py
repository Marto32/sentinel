"""
This module should house all of the configurations needed for the clients
to connect to the api.
"""
import os

# Define the endpoints that will
# be called via the client
endpoints = {
    'notify': os.environ.get('NOTIFY_ENDPOINT'),
    'log': os.environ.get('LOG_ENDPOINT'),
    }

# Define the BCM pins that are used
# by each client
pin_map_arg_parse = os.environ.get('PIN_MAP').split(':')
PIN_MAP = [k.split(',') for k in pin_map_arg_parse if k]
gpio_pin_map = {k:int(v) for k,v in dict(PIN_MAP).items()}

# Identify this particular client
# so it knows which monitor and pins to use
# client_identifier = 'example'
client_identifier = os.environ.get('CLIENT_NAME')

# Set the notification timezone
notify_tz = os.environ.get('TIMEZONE')

# Sentinel secret key
SENTINEL_SECRET_KEY = os.environ.get('SENTINEL_SECRET_KEY')
