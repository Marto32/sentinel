"""
This module should house all of the configurations needed for the clients
to connect to the api.
"""

# Define the endpoints that will
# be called via the client
endpoints = {
    'notify': '',
    'log': '',
    }

# Define the BCM pins that are used
# by each client
gpio_pin_map = {
    # 'example': 15
    }

# Identify this particular client
# so it knows which monitor and pins to use
# client_identifier = 'example'
client_identifier = ''

# Set the notification timezone
notify_tz = ''
