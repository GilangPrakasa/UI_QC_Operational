import requests,time
import Utility as U

Address_Reset_Event = 'http://192.168.4.1:2516/log?page=reset'
wdt_function_result = []

def reset_log():
    headers = U.headers()
    response = requests.get(Address_Reset_Event, headers=headers)
    if response.status_code == 200:
        U.printG('============== RESET EVENT LOG DONE ===============')
    else:
        U.printR(response.text)
        U.printR('============= RESET EVENT LOG FAILED ==============')
        

def run_motor(Address_Run):
    headers = U.headers()
    post_run_start = {
        'command': '1'
    }
    response = requests.post(Address_Run, headers=headers, data=post_run_start)
    if response.status_code == 200:
        # U.printG('Run motor success')
        pass
    else:
        U.printR('Run motor failed!')
        U.printR(response.text)

def Simulate_hang(Address_Alert,Address_Run):
    reset_log()
    run_motor(Address_Run)
    params = {
        'isHang': '1'
    }
    U.printC('============= START TEST WDT FUNCTION =============')
    response = requests.post(Address_Alert, params=params)
    if response.status_code == 200:
        U.printY('============= PLEASE MONITORING COBOX =============')
        U.printY('================ UNTIL RESTARTING =================')
        U.printY('======== TEST SUCCESS IF COBOX RESTARTING =========')
        wdt_function_result.append("PASS")
    else:
        U.printR('============== SIMULATE HANG FAILED ===============')
        U.printR(response.text)
        # U.Percentage_Failed.append("TEST WDT FUNCTION")

# Simulate_hang(U.Address_Alert,U.Address_Run)
