"""Send abrp."""

from .abrp.abrp_class import abrp_class
from pprint import pprint

def send_abrp(config, data):
    abrp = abrp_class(token=config['abrp']['token'], debug_output=print)
    result = abrp.send_data(data)
    print('>>>>>>>>')
    pprint(result)
    print('<<<<<<<<')
