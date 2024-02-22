import requests
import time
import Utility as U

read_current_result = []

def run_motor(Address_Run):
    headers = U.headers()
    post_run_start = {
        'command': '1'
    }
    response_0 = requests.post(Address_Run, headers=headers, data=post_run_start)
    if response_0.status_code == 200:
        # U.printG('Run motor success')
        pass
    else:
        U.printR('Run motor failed!')
        U.printR(response_0.text)
    
    time.sleep(6)

    post_run_stop = {
        'command': '0'
    }
    response_1 = requests.post(Address_Run, headers=headers, data=post_run_stop)
    if response_1.status_code == 200:
        # U.printG('Stop motor success')
        time.sleep(1)
    else:
        U.printR('Stop motor failed!')
        U.printR(response_1.text)

def Read_Current(Address_Current, Address_Run):
    run_motor(Address_Run)
    headers = U.headers()
    response = requests.get(Address_Current, headers=headers)
    U.printG('============= START TEST READ CURRENT =============')
    time.sleep(1)
    if response.status_code == 200:
        # U.printG('Get current successful!')
        Read_Json = response.json()
        Dosing_current = float(Read_Json['dosing_max'])
        Thrower_current = float(Read_Json['thrower_max'])
        if Dosing_current <= 1 and Thrower_current <= 1:
            U.printY(f"Dosing current in range   : {Dosing_current}")
            U.printY(f"Thrower current in range  : {Thrower_current}")
            U.printG('============ READ CURRENT TEST SUCCESS ============')
            read_current_result.append("PASS")
        else:
            U.printY(f"Dosing current not in range   : {Dosing_current}")
            U.printY(f"Thrower current not in range  : {Thrower_current}")
            U.printR('============= READ CURRENT TEST FAILED ============')
            U.Percentage_Failed.append("READ CURRENT")
    else:
        U.printR('Get current failed!')
        U.printR(response.text)

# Read_Current(U.Address_Current, U.Address_Run)