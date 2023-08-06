""" Loop. """
import time

def data_loop(idle_wait=15, drive_wait=5, charge_wait=5):
    last_km = None
    from .fhs_enyaq_data import get_instruments_with_timeout
    from .config import get_config
    from .abrp_send import send_abrp
    config = get_config()
    while True:
        # run
        print('get instruments.')
        instruments = get_instruments_with_timeout(config)
        if instruments is not None:
            send_abrp(config, instruments)
            sleep_time = idle_wait * 60
            if last_km is None:
                last_km = instruments['Electric range']
            if instruments['Charging'] == 1:
                sleep_time = charge_wait * 60
                print('charging.')
            elif last_km != instruments['Electric range']:
                sleep_time = drive_wait * 60
                print('driving.')
            last_km = instruments['Electric range']
            time.sleep(sleep_time)
        else:
            print('no instruments returned.')
            time.sleep(120)


