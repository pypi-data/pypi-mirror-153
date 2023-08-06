import time
import requests

# get car types:
# curl https://api.iternio.com/1/tlm/get_carmodels_list | jq . | grep skoda
#      "Skoda;ENYAQ iV;50 (alpha)": "skoda:enyaq:21:52:meb"
#      "Skoda;ENYAQ iV;60 (alpha)": "skoda:enyaq:21:58:meb"
#      "Skoda;ENYAQ iV;80 (alpha)": "skoda:enyaq:21:77:meb"
#      "Skoda;ENYAQ iV;80x (alpha)": "skoda:enyaq:21:77:meb:x"
#      "Skoda;ENYAQ iV;RS (alpha)": "skoda:enyaq:21:77:meb:rs"
#      "Skoda;ENYAQ iV;portline (alpha)": "skoda:enyaq:21:77:meb:sportline"


class abrp_class:
    def __init__(self, token, api_key='c626070c-1c8d-4003-bc76-6de223b44679', url='https://api.iternio.com/1/', car_type='skoda:enyaq:21:77:meb', debug_output=None):
        self.token = token
        self.api_key = api_key
        self.url = url
        self.car_type = car_type
        self.debug_output = debug_output
        self.fail_output = print

    def debug(self, str):
        if self.debug_output != None:
            self.debug_output(str)

    def fail(self, str):
        if self.fail_output != None:
            self.fail_output(str)

    def create_data(self, input_data):
        output_data = {}
        output_data['utc'] = int(time.time())
        output_data['soc'] = input_data['Battery level'] 
        output_data['car_model'] = self.car_type
        output_data['is_charging'] = input_data['Charging']
        output_data['est_battery_range'] = input_data['Electric range']
        output_data['power'] = int(input_data['Charging power'] / -1000)
        self.debug_output(str(output_data))
        return output_data

    def send(self, output_data):
        try:
            headers = {"Authorization": f"APIKEY {self.api_key}"}
            data = {"tlm": output_data}
            result = requests.post(f"{self.url}/tlm/send?token={self.token}", headers=headers, json=data)
        except Exception as e:
            self.fail(f'post issue: {str(e)}')
        return result


    def send_data(self, input_data):
        output_data = self.create_data(input_data)
        return self.send(output_data)
