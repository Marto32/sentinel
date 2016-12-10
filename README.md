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

