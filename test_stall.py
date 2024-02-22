import requests
import time
import Utility as U

prep_stall_result = []

def Set_Current(Address_Current):
    headers = U.headers()
    Post_Current = {
        "thrower_overcurrent": 12.5,
        "dosing_overcurrent": 10,
    }
    response0 = requests.post(Address_Current, headers=headers, json=Post_Current)
    if response0.status_code == 200:
        # U.printG('Post DEFAULT current successful!')
        # print(response0.json())
        time.sleep(1)
    else:
        U.printR('Post DEFAULT current failed!')
        U.printR(response0.text)
    
    time.sleep(1)

def Run_Cobox(Address_Run):
    headers = U.headers()
    POST_RUN_START = {
        'command': '1'
    }
    response0 = requests.post(Address_Run, headers=headers, data=POST_RUN_START)
    if response0.status_code == 200:
        # U.printG('Post RUN_MOTOR_PWM successful!')
        pass
    else:
        U.printR('Post RUN_MOTOR_PWM failed!')
        U.printR(response0.text)
    
    time.sleep(6)

    POST_RUN_STOP = {
        'command': '0'
    }
    response1 = requests.post(Address_Run, headers=headers, data=POST_RUN_STOP)
    if response1.status_code == 200:
        # U.printG('POST STOP_MOTOR_PWM successful!')
        time.sleep(3)
        
    else:
        U.printR('POST STOP_MOTOR_PWM current failed!')
        U.printR(response1.text)

def Read_Current(Address_Run,Address_Current):
    Run_Cobox(Address_Run)
    headers = U.headers()
    response = requests.get(Address_Current, headers=headers)
    if response.status_code == 200:
        # U.printG('Request current successful!')
        Read_Json = response.json()
        U.printG('================== SETTING RESULT =================')
        # print(Read_Json)
        Dosing_current = float(Read_Json['dosing_max'])
        U.printY(f"Dosing Max = {Dosing_current}")
        Thrower_current = float(Read_Json['thrower_max'])
        U.printY(f"Thrower Max = {Thrower_current}")
        Post_Limit(Thrower_current,Dosing_current,Address_Current)
    else:
        U.printR('Request failed!')
        U.printR(response.text)

def Post_Limit(T,D,Address_Current):
    if 0 <= T < 1: 
        T_limit = T + 0.4
        print(f"T = {T_limit}")
    if 0 <= D < 1:
        D_limit = D + 0.4
        print(f"D = {D_limit}")
    if 1 <= T <= 2:
        T_limit = T + 0.7
        print(f"T = {T_limit}")
    if 1 <= D <= 2:
        D_limit = D + 0.7
        print(f"D = {D_limit}")
    if 2 < T <= 10:
        T_limit = T + 1
        print(f"T = {T_limit}")
    if 2 < D <= 10:
        D_limit = D + 1
        print(f"D = {D_limit}")
        
    headers = U.headers()
    Post_Current = {
        "thrower_overcurrent": T_limit,
        "dosing_overcurrent": D_limit
    }
    response0 = requests.post(Address_Current, headers=headers, json=Post_Current)
    if response0.status_code == 200:
        # U.printG('Post LIMIT current successful!')
        # print(response0.json())
        time.sleep(1)
    else:
        U.printR('Post LIMIT current failed!')
        U.printR(response0.text)

def Run_Stall(Address_Run,Address_Current):
    Set_Current(Address_Current)
    Read_Current(Address_Run,Address_Current)
    Run_Cobox(Address_Run)
    time.sleep(2)
    headers = U.headers()
    response = requests.get(Address_Current, headers=headers)
    if response.status_code == 200:
        # U.printG('Request current successful!')
        Read_Json = response.json()
        # print(Read_Json)
        Dosing_current = float(Read_Json['dosing_overcurrent'])
        U.printY(f"Dosing Overcurrent = {Dosing_current}")
        Thrower_current = float(Read_Json['thrower_overcurrent'])
        U.printY(f"Thrower Overcurrent = {Thrower_current}")
        U.printG('=============== SETTING RESULT DONE ===============')
        prep_stall_result.append("PASS")
    else:
        U.printR('Request failed!')
        U.printR(response.text)
        U.printR('============== SETTING RESULT FAILED ==============')
    
# Run_Stall(U.Address_Run,U.Address_Current)