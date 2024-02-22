import requests
import time
import Utility as U
# ============= BOOLEAN =============
true = 1
false = 0
# ========== STORAGE STRING =========

thrower_pwm_result = []
list_res           = []

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

def set_current(Address_Current):
    global Get_Current
    headers = U.headers()
    post_current = {
        "thrower_overcurrent": 12.5,
        "dosing_overcurrent": 10,
    }
    response = requests.post(Address_Current, headers=headers, json=post_current)
    if response.status_code == 200:
        # U.printG('Set current success')
        time.sleep(1)
    else:
        U.printR('Set current failed!')
        U.printR(response.text)

def thrower_setting(Address_Setting, Address_Run, Address_Current, pwm):
    headers = U.headers()
    post_setting = {
        "feed_debit": 100000,
        "thrower_extra": 3,
        "enable_button": true,
        "activated": true,
        "motor_power": pwm,
        "pond_id": "null"
    }
    response = requests.post(Address_Setting, headers=headers, json=post_setting)
    # U.printG(f'========== TEST FEED THROWER DISTANCE {pwm} ==========')
    if response.status_code == 200:
        # U.printG('Set PWM success')
        time.sleep(1)
        thrower_handling(Address_Setting, Address_Run, Address_Current, pwm)
    else:
        # U.printR('Set PWM failed!')
        # U.printR(response.text)
        U.Percentage_Failed.append(f"FEED THROWER DISTANCE {pwm}")

def thrower_handling(Address_Setting, Address_Run, Address_Current, pwm):
    set_current(Address_Current)
    run_motor(Address_Run)
    headers = U.headers()
    response = requests.get(Address_Setting, headers=headers)
    if response.status_code == 200:
        # U.printG('Get PWM successful!')
        read_json_res = response.json()
        motor_power_res = str(read_json_res['motor_power'])
        if motor_power_res == f"{pwm}":
            U.printY(f"PWM MATCH R: {motor_power_res} E: {pwm}")
            # U.printG(f"====== FEED THROWER DISTANCE TEST SUCCESS {pwm} ======")
            list_res.append(pwm)
        else:
            U.printR(f"PWM MATCH R: {motor_power_res} E: {pwm}")
            # U.printR(f"====== FEED THROWER DISTANCE TEST FAILED  {pwm} ======")
    else:
        U.printR('Get PWM failed!')
        U.printR(response.text)
        U.printR("======== FEED THROWER DISTANCE TEST FAILED ========")

def thrower_pwm(Address_Setting, Address_Run, Address_Current):
    find_res = U.PWM
    value    = U.PWM
    U.printG(f'=========== TEST FEED THROWER DISTANCE ============')
    for pwm in value:
        thrower_setting(Address_Setting, Address_Run, Address_Current, pwm)

    existence_check = all(find_res in list_res for find_res in find_res)
    if existence_check:
        thrower_pwm_result.append("PASS")
        U.printG("========= FEED THROWER DISTANCE TEST DONE =========")
    else:
        U.printR("======== FEED THROWER DISTANCE TEST FAILED ========")
    
    U.printR((f"============ PLEASE UNPLUG CABLE MOTOR ============"))
    time.sleep(1)   

# thrower_pwm(U.Address_Setting, U.Address_Run, U.Address_Current)