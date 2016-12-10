"""
This module should house all of the configurations needed for the API.
For example, all endpoints, credentials, etc.
"""

# Set an endpoint dictionary which will be used by the API
endpoints = {
        'notify': '/sentinel/v1/notify',
        'log'   : '/sentinel/v1/log'
        }

# Instapush objects
push_objects = {

        'autome_app': {
            'app_name': 'autome',
            'event_weatherme': 'weatherme'
            },

        'sentinel_app': {
            'app_name':'sentinel'
            }
        }
