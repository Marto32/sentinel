# Sentinel
Personal home monitoring system

## Overview
Sentinel is meant to monitor various aspects of a users home. At the time of this writing, the system is limited to monitoring the state of a selected door(s) in the home. It is being built extensibly so it can incorporate other types of monitoring (temperature, humidity, light, motion, etc.)

## Operational Flow
The system consists of physical sensors connected to a network of Raspberry Pi's which speak to a RESTful API in the cloud. This API logs information received from the physical monitors and notifies the user:

 * Sensor is activated
 * RPi initiates an onboard script
 * Script tracks time and calls API
 * API notifies user and logs info provided

## Setup
Sentinel uses [Twilio](https://www.twilio.com/sms) to send notifications via SMS. You can sign up for a free account on their site. In addition, the following environment variables need to be defined so Sentinel can access your Twilio account:

```
TWILIO_ACCOUNT_SID          The account service ID provided by Twilio
TWILIO_AUTH_TOKEN           Authorization token provided by Twilio
TWILIO_SOURCE_PHONE         Must be in the format +1xxxxxxxxxx
TWILIO_DESTINATION_PHONE    Same format as above
```

In addition to your twilio credentials, Sentinel also needs some information regarding your Raspberry Pi:
```
PIN                         Defines the BCM pin on the RPi that is used (more info below)
TIMEZONE                    Used to convert notification times to your time zone
```

