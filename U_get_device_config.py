import requests, time
address = "http://192.168.4.1:2516/get_device_config"

def get_device_config():
    response = requests.get(address)
    if response.status_code == 200:
        read_json = response.json()
        token = str(read_json['feeder']['token'])
        uuid  = str(read_json['feeder']['uuid'])
        jwt   = str(read_json['feeder']['jwt'])
        print(f"token : {token}")
        print(f"uuid  : {uuid}")
        print(f"jwt   : {jwt}")
    else:
        print(response.json)
    return token

# get_device_config()