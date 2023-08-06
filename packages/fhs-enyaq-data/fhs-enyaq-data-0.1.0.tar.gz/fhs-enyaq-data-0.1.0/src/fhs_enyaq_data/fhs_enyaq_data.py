"""Main module."""

from fhs_enyaq_data.skoda_class.skoda_class import skoda_class
import signal

def main(config):
    """ Skoda. """
    skoda = skoda_class(config=config['skoda'])
    skoda.list_cars()


def get_vehicle_data(config):
    if 'vehicle_vin' not in config['skoda'] or config['skoda']['vehicle_vin'] == '':
        vehicle_vin = None
    else:
        vehicle_vin = config['skoda']['vehicle_vin']
    result = skoda.get_battery_level(vehicle_vin)
    skoda = skoda_class(config=config['skoda'])
    print(f"{result=}")


def print_instruments(config):
    if 'vehicle_vin' not in config['skoda'] or config['skoda']['vehicle_vin'] == '':
        vehicle_vin = None
    else:
        vehicle_vin = config['skoda']['vehicle_vin']
    skoda = skoda_class(config=config['skoda'])
    result = skoda.print_instruments(vehicle_vin)

def get_instruments(config):
    if 'vehicle_vin' not in config['skoda'] or config['skoda']['vehicle_vin'] == '':
        vehicle_vin = None
    else:
        vehicle_vin = config['skoda']['vehicle_vin']
    skoda = skoda_class(config=config['skoda'])
    result = skoda.get_instruments(vehicle_vin)
    return (result)

def get_instruments_with_timeout(config, timeout=60):
    class TimeOutException(Exception):
        pass

    def alarm_handler(signum, frame):
        raise TimeOutException()

    signal.signal(signal.SIGALRM, alarm_handler)
    signal.alarm(timeout)

    try:
        result = get_instruments(config)
    except TimeOutException as ex:
        result = None
    signal.alarm(0)
    return result

