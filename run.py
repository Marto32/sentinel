from retrying import retry
from util.switch_helper import DoorMonitor, StatefulSwitch
from settings import PIN 


@retry(stop_max_attempt_number=30, wait_fixed=1000)
def monitor(switch: StatefulSwitch) -> None:
    """
    A method used to monitor a switch object.
    """
    while True:
        switch.route_action()


if __name__ == '__main__':
    front_door = DoorMonitor(
        name='front_door',
        gpio_pin=PIN
    )

    monitor(front_door)

