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
PIN_MAP = os.environ.get('PIN_MAP').split(',')
gpio_pin_map = {
    k:PIN_MAP[i+1] for k,i in enumerate(PIN_MAP)
    }

# Identify this particular client
# so it knows which monitor and pins to use
# client_identifier = 'example'
client_identifier = os.envorn.get('CLIENT_NAME')

# Set the notification timezone
notify_tz = os.environ.get('TIMEZONE')

# Sentinel secret key
SENTINEL_SECRET_KEY = os.environ.get('SENTINEL_SECRET_KEY')
