import abc
import requests
from datetime import datetime, timedelta
from dateutil import tz

from client.util.client_config import notify_tz

import RPi.GPIO as gpio


class Trigger(object):
    """
    The base class for all triggers.
    """

    def __init__(self):
        pass


class BinaryTrigger(Trigger):
    """
    A binary trigger.

    This object is meant to be fired based on a binary trigger.
    """

    def __init__(self, name, gpio_pin, notify_endpoint, log_endpoint, seconds_threshold=30):
        """
        :param name: str, the name of the trigger (used in notifications and logging)
        :param gpio_pin: int, the gpio pin number
        :param notify_endpoint: str, the endpoint to hit for notifications
        :param log_endpoint: str, the endpoint to hit to log events
        :param seconds_threshold: int, the threshold used to notify the user
        :param start_time: datetime, placeholder for the time the trigger is activated
        :param state: bool, the initial state of the trigger
        """
        Trigger.__init__(self)
        self.name = name
        self.gpio_pin = gpio_pin
        self.notify_endpoint = notify_endpoint
        self.log_endpoint = log_endpoint
        self.seconds_threshold = float(seconds_threshold)
        self.start_time = None
        self.state = False # Initializes the state of the trigger

        # Set the notification timezone (to convert to
        # from UTC)
        self.notification_tz = tz.gettz(notify_tz)

        # Set threshold interval so the user is not
        # continuously notified after the threshold is passed
        self.seconds_threshold_interval = self.seconds_threshold

    def notify(self, data):
        """
        Method to call the api to notify the user of the trigger state.
        :param data: dict, a dictionary including data needed to notify the user
            with required key 'event_name' and 'trackers'

        Example:
        {
            'event_name': 'name'
            'trackers': {
                'email': 'myemail'
            }
        }
        """
        return requests.post(self.notify_endpoint, json=data)

    def log(self, data):
        """
        Method to call the api to log the trigger state
        :param data: dict, a dictionary containing the data needed to log the event
            with required keys 'event_name', 'time'

        Example:
        {
            'event_name': 'name',
            'time': datetime
        }
        """
        return requests.post(self.log_endpoint, data)

    def calculate_time_on(self):
        """
        Method that calculates the time the trigger is 'open'
        (e.g. the time it has been either on or off)

        :returns: float, total seconds the trigger has been in one state or 'open'
            format is [seconds].[microseconds]
        """
        duration = datetime.utcnow() - self.start_time
        return round(duration.total_seconds(), 2)

    def should_notify(self):
        """
        A helper method to check if we should notify the end-user.

        :returns: bool, True or False
        """
        if self.calculate_time_on() >= self.seconds_threshold_interval:
            self.seconds_threshold_interval *= 2
            return True
        else:
            return False

    def configure_gpio_input(self):
        ## set GPIO mode to BCM
        ## this takes GPgpio.number instead of pin number
        gpio.setmode(gpio.BCM)
        ## use the built-in pull-up resistor
        gpio.setup(self.gpio_pin, gpio.IN, pull_up_down=gpio.PUD_UP)  # activate input with PullUp

    def convert_timezone_for_notification(self, utc_time):
        """
        :param utc_time: datetime, The time in UTC as a datetime object
        :returns: str, The time to input in notify
        """
        utc = utc_time.replace(tzinfo=tz.tzutc())
        converted_datetime = utc.astimezone(self.notification_tz)
        return converted_datetime.strftime('%H:%M:%S')

    def monitor(self):
        """
        method that should track status of the trigger and take action according
        to its state.
        """
        raise NotImplementedError


class DoorMonitor(BinaryTrigger):

    def route_action(self):
        """
        Used to route actions based on the logic in the
        monitor method.
        """
        if gpio.input(self.gpio_pin) and not self.state:
            # set the start time
            self.start_time = datetime.utcnow()

            # Inform the end-user that the front door has been opened
            # and Log the event
            payload = {
                'event_name': 'front_door_opened',
                'trackers': {'time': self.convert_timezone_for_notification(self.start_time)
                    }
                }

            self.notify(payload)

            # Prep the log payload
            log_load = {
                'trigger_name': self.name,
                'event_name': payload.get('event_name'),
                'time': self.start_time.strftime('%Y%m%d %H:%M:%S')
                }

            self.log(log_load)

            # Set state to active now that the trigger has been fired
            # and 'opened'
            self.state = True

        elif gpio.input(self.gpio_pin) and self.state:
            # check time
            if self.should_notify():
                payload = {
                    'event_name': 'front_door_open_long',
                    'trackers': {'seconds': self.calculate_time_on()
                        }
                    }

                self.notify(payload)

        elif not gpio.input(self.gpio_pin) and self.state:
            # the trigger has been fired due to a 'close' event
            close_time = datetime.utcnow()

            # Prep the notificaiton payload
            payload = {
                'event_name': 'front_door_closed',
                'trackers': {'time': self.convert_timezone_for_notification(close_time)
                    }
                }

            self.notify(payload)
            # Prep the log payload
            log_load = {
                'trigger_name': self.name,
                'event_name': payload.get('event_name'),
                'time': close_time.strftime('%Y-%m-%d|%H:%M:%S')
                }

            self.log(log_load)
            self.state = False

            # Reset start time
            self.start_time = None

            # Reset the threshold interval
            self.seconds_threshold_interval = self.seconds_threshold

        else:
            pass

    def schedule_check(self):
        """
        A method to check whether or not the device should
        be running.
        """
        # TODO - Implement scheduling logic
        return True

    def monitor(self):
        """
        This method opens an infinite loop to continuously monitor
        the trigger. It can be controlled automatically using the
        `schedule_check` method above.
        """
        self.configure_gpio_input()
        while True:
            if self.schedule_check():
                self.route_action()


