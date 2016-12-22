from client.util.trigger_helper import FrontDoorMonitor
from client.util.client_config import endpoints, gpio_pin_map, client_identifier

front_door = FrontDoorMonitor('front_door', gpio_pin_map.get('front_door'),
    endpoints.get('notify'), endpoints.get('log'))

if __name__ == '__main__':
    # Define the monitor_map so the client can call
    # specific monitoring objects based on its designation
    monitor_map = {
        'front_door': front_door
        }

    # Trigger montioring for this client
    monitor_map.get(client_identifier).monitor()

