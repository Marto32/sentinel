import attr
import RPi.GPIO as gpio

from datetime import datetime, timedelta
from dateutil import tz

from settings import notify_tz
from contrib.twilio_api_helper import SendNotification
from typing import Optional


@attr.s
class StatefulSwitch(object):
    """
    """

    name: str = attr.ib()
    gpio_pin: int = attr.ib()
    gpio_configured: bool = attr.ib(default=False)
    seconds_threshold: int = attr.ib(default=30)
    seconds_threshold_interval: Optional[int] = attr.ib(default=None)
    start_time: Optional[datetime] = attr.ib()
    wakeful_state: bool = attr.ib(default=False)
    notification_tz: tz.tzlocal = attr.ib(default=tz.gettz(notify_tz))

    def configure_gpio_input(self) -> None:
        """
        This method setups up a Raspberry Pi GPIO input
        using the BCM mode so we can use a gpio number instead of
        a pin number.

        This method also configures the inputs to use the
        built in pull-up resistor.
        """
        if not self.gpio_configured:
            gpio.setmode(gpio.BCM)
            gpio.setup(
                self.gpio_pin,
                gpio.IN,
                pull_up_down=gpio.PUD_UP
            )
            self.gpio_configured = True

    def notify(self, message: str): # TODO(Add type hinting)
        """
        Notifies the user of the switch's state via one of the pre
        defined message methods.
        """
        return SendNotification(message).emit()

    def log(self, data: dict) -> None:
        raise NotImplementedError

    def calculate_time_open(self) -> float:
        """
        Calculates the time the switch has been open.
        """
        duration = datetime.utcnow() - self.start_time
        return round(duration.total_seconds(), 2)

    def wakeful_state_duration_exceeds_threshold(self) -> bool:
        """
        Determines if the time the switch has been open exceeds the
        defined threshold (`seconds_threshold`).
        """
        # Set the threshold interval value if this is the first check
        if self.seconds_threshold_interval is None:
            self.seconds_threshold_interval = self.seconds_threshold
            return False

        # Else perform the actual check
        elif self.calculate_time_open() >= self.seconds_threshold_interval:
            self.seconds_threshold_interval *= 2
            return True
        else:
            return False

    def convert_timezone_for_notification(self, utc_time: datetime) -> str:
        """
        Converts the time to the local timezone (defined in the settings file).
        """
        utc: datetime= utc_time.replace(tzinfo=tz.tzutc())
        converted_datetime = utc.astimezone(self.notification_tz)
        return converted_datetime.strftime('%H:%M:%S')

    def switch_opened_message(self, time: str) -> str:
        """
        The message used to notify the user
        when the switch is first opened.
        """
        raise NotImplementedError

    def switch_open_message(self, time: str) -> str:
        """
        The message used to notify the user
        when the switch has remained open.
        """
        raise NotImplementedError

    def switch_closed_message(self, time: str) -> str:
        """
        The message used to notify the user
        when the switch has been closed.
        """
        raise NotImplementedError

    def route_action(self) -> None:
        """
        Uses the current state of the switch and the feedback from
        the Raspberry Pi's GPIO pins to take some action (this may be to
        notify the user, etc.)
        """
        self.configure_gpio_input()
        switch_active: bool = gpio.input(self.gpio_pin)

        # switch activated and opened for the first time
        if switch_active and not self.wakeful_state:
            self.start_time = datetime.utcnow()
            self.notify(self.switch_opened_message(self.start_time.strftime('%H:%M:%S')))
            self.wakeful_state = True

        # switch remains active and open
        elif switch_active and self.wakeful_state:
            if self.wakeful_state_duration_exceeds_threshold():
                self.notify(self.switch_open_message(
                    str(self.seconds_threshold_interval)
                ))

        # switch closed
        elif not switch_active and self.wakeful_state:
            close_time: datetime = datetime.utcnow()
            self.notify(self.switch_closed_message(
                close_time.strftime('%H:%M:%S')))
            self.wakeful_state = False
            self.start_time = None
            self.seconds_threshold_interval = self.seconds_threshold


class DoorMonitor(StatefulSwitch):

    def switch_opened_message(self, time: str) -> str:
        return f'The door was opened at {time}.'

    def switch_open_message(self, time: str) -> str:
        return f'The door has been open for {time} seconds.'

    def switch_closed_message(self, time: str) -> str:
        return f'The door was closed at {time}.'

