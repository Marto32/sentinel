"""
This module should house all of the configurations
"""
import os

# Twilio Credentials
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')

# Phone numbers must be in the format +1xxxxxxxxxx
TWILIO_SOURCE_PHONE = os.environ.get('TWILIO_SOURCE_PHONE')
TWILIO_DESTINATION_PHONE =os.environ.get('TWILIO_DESTINATION_PHONE')

# Define the BCM pin that should be used
PIN = int(os.environ.get('PIN'))

# Set the notification timezone
notify_tz = os.environ.get('TIMEZONE')

