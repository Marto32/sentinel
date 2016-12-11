import abc
import requests
from datetime import datetime, timedelta

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

    def __init__(self, name, gpio_trigger, notify_endpoint, log_endpoint, seconds_threshold=120):
        """
        :param name: str, the name of the trigger (used in notifications and logging)
        :param gpio_trigger: the gpio trigger
        :param notify_endpoint: str, the endpoint to hit for notifications
        :param log_endpoint: str, the endpoint to hit to log events
        :param seconds_threshold: int, the threshold used to notify the user
        :param start_time: datetime, placeholder for the time the trigger is activated
        :param state: bool, the initial state of the trigger
        """
        Trigger.__init__(self)
        self.name = name
        self.gpio_trigger = gpio_trigger
        self.notify_endpoint = notify_endpoint
        self.log_endpoint = log_endpoint
        self.seconds_threshold = float(seconds_threshold)
        self.start_time = None
        self.state = False # Initializes the state of the trigger

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
        duration = datetime.now() - self.start_time
        return duration.total_seconds()

    def should_notify(self):
        """
        A helper method to check if we should notify the end-user.

        :returns: bool, True or False
        """
        return True if self.calculate_time_on() >= self.seconds_threshold else False

    def monitor(self):
        """
        method that should track status of the trigger and take action according
        to its state.
        """
        raise NotImplementedError


class FrontDoorMonitor(BinaryTrigger):

    def monitor(self):
        while True
            if gpio.input(self.gpio_trigger) and not self.state:
                # set the start time
                self.start_time = datetime.now()

                # Inform the end-user that the front door has been opened
                # and Log the event
                payload = {
                    'event_name': 'front_door_opened',
                    'trackers': {'time': self.start_time.strftime('%H:%M:%S')
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

            elif gpio.input(self.gpio_trigger) and self.state:
                # check time
                if self.should_notify():
                    payload = {
                        'event_name': 'front_door_open_long',
                        'trackers': {'seconds': self.calculate_time_on()
                            }
                        }

                    self.notify(payload)

            elif not gpio.input(self.gpio_trigger) and self.state:
                # the trigger has been fired due to a 'close' event
                close_time = datetime.now()

                # Prep the notificaiton payload
                payload = {
                    'event_name': 'front_door_closed',
                    'trackers': {'time': close_time.strftime('%H:%M:%S')
                        }
                    }

                self.notify(payload)
                # Prep the log payload
                log_load = {
                    'trigger_name': self.name,
                    'event_name': payload.get('event_name'),
                    'time': close_time.strftime('%Y%m%d %H:%M:%S')
                    }

                self.log(log_load)
                self.state = False

                # Reset start time
                self.start_time = None

            else:
                pass

