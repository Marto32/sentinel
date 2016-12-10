import abc
from datetime import datetime, timedelta


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

    def __init__(self, name, notify_on, notify_off, seconds_threshold=120):
        """
        :param name: str, the name of the trigger (used in notifications and logging)
        :param notify_on: str, instapush interface or api interface, tpd
        :param notify_off: str, instapush interface or api interface, tpd
        :param seconds_threshold: int, the threshold used to notify the user
        :param start_time: datetime, placeholder for the time the trigger is activated
        :param state: bool, the initial state of the trigger
        """
        Trigger.__init__(self)
        self.name = name
        self.notify_on = notify_on
        self.notify_off = notify_off
        self.seconds_threshold = float(seconds_threshold)
        self.start_time = None
        self.state = False # Initializes the state of the trigger

    def notify(self):
        """
        Method to call the api to notify the user of the trigger state.
        """
        raise NotImplementedError

    def log(self):
        """
        Method to call the api to log the trigger state
        """
        raise NotImplementedError

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
        while True
            if gpio.input(trigger) and not self.state:
                # set the start time
                self.start_time = datetime.now()

                # Inform the end-user that this trigger has been activated
                # and Log the event
                self.notify()
                self.log()

                # Set state to active now that the trigger has been fired
                # and 'opened'
                self.state = True

            elif gpio.input(trigger) and self.state:
                # check time
                if self.should_notify():
                    self.notify()

            elif not gpio.input(trigger) and self.state:
                # the trigger has been fired due to a 'close' event
                self.notify()
                self.log()
                self.state = False

                # Reset start time
                self.start_time = None

            else:
                pass

