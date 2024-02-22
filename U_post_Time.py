import time
from datetime import datetime
import requests
# ============= BOOLEAN =============
true = 1
false = 0
# ============= ENDPOINT ============
Address_Time = 'http://192.168.4.1:2516/time'

current_epoch_time = int(time.time())
converted_datetime = datetime.utcfromtimestamp(current_epoch_time)

print("Current Epoch Time:", current_epoch_time)
print("Converted Date and Time:", converted_datetime)

def Post_Time():
    global Address_Time
    POST_TIME = {
        'timestamp': f'{current_epoch_time}'
    }
    headers = {
        'token': '4-WZKgT6ANQQrT'
    }
    response0 = requests.post(Address_Time, headers=headers, data=POST_TIME)
    if response0.status_code == 200:
        print('Post Time successful!')
        print(response0.json())
    else:
        print('Post Time failed!')
        print(response0.text)

try:
    Post_Time()
    time.sleep(10)

except KeyboardInterrupt and Exception :
    Interrupt = True
    print("ERROR DETECTED")