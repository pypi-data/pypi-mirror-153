import time
from tuyaface.tuyaclient import TuyaClient

def on_status(data: dict, tuyatype=None):
    print(data)

def on_connection(value: bool, tuyatype=None):
    print(value)

device = {
    'protocol': '3.3', # 3.1 | 3.3
    'deviceid': '047555462cf432a18791',
    'localkey': '9b7eeb55d0c7819e',
    'ip': '10.0.1.45',            
}

client = TuyaClient(device, on_status, on_connection)
client.start()

data = client.status()
while True:
    print('Wait...')
    time.sleep(2)

#client.set_state(!data['dps']['1'], 1) #toggle
client.stop_client()
