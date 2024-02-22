import requests
import time
from datetime import datetime
import Utility as U

feed_schedule_result = []
list_res         = []
find_res         = ["Time Stamp","Amount","Trigger"]

def check(data, string, expect):
    if data == expect:
        U.printY(f"{string} : True   R: {data}  E: {expect}")
        list_res.append(string)
    else:
        U.printR(f"{string} : False  R: {data}  E: {expect}",)

def Post_Time(Address_Time):
    headers = U.headers()
    current_epoch_time = int(time.time())
    converted_datetime = datetime.fromtimestamp(current_epoch_time)
    # U.printC(f"Current Epoch Time : {current_epoch_time}")
    # U.printC(f"Converted Time     : {converted_datetime}")
    POST_TIME = {
        'timestamp': f'{current_epoch_time}'
    }
    response = requests.post(Address_Time, headers=headers, data=POST_TIME)
    if response.status_code == 200:
        # U.printG('Post Time success')
        pass
    else:
        U.printR('Post Time failed!')
        U.printR(response.text)

def time_now():
    time_now = datetime.now().strftime("%H:%M:%S")
    date_time = f'01.01.1970 {time_now}'
    pattern = '%d.%m.%Y %H:%M:%S'
    epoch = int(time.mktime(time.strptime(date_time, pattern)))
    # U.printC(f"Time schedule target {time_now} || {epoch}")
    return epoch

def Feeding_schedule(Address_Schedules,Address_Time,Address_crawlback):
    Post_Time(Address_Time)
    current_epoch_time = int(time.time())
    target_schedule = current_epoch_time + 6
    converted_datetime = datetime.fromtimestamp(target_schedule)
    # U.printC(f"Schedule target    : {converted_datetime} || {target_schedule}")
    schedule_time = time_now() + 6
    # U.printC(schedule_time)
    POST_SCHEDULE = {
        "count": 1,
        "schedules": [
            {
                "duration_pause": 'null',
                "duration_run": 'null',
                "feed_target": 1000,
                "time_quota": 'null',
                "time_start": schedule_time
            }
        ]
    }
    headers = U.headers()
    response_0 = requests.post(Address_Schedules, headers=headers, json=POST_SCHEDULE)
    U.printG('========== START TEST FEEDING SCHEDULE ============')
    if response_0.status_code == 200:
        # U.printG('Post schedule success')
        pass
    else:
        U.printR('Post schedule failed!')
        U.printR(response_0.text)
    
    response_1 = requests.get(Address_Schedules, headers=headers)
    if response_1.status_code == 200:
        # U.printG('Get schedule success')
        Read_Json_1 = response_1.json()
        time_start  = str(Read_Json_1['schedules'][0]['time_start'])
        feed_target = str(Read_Json_1['schedules'][0]['feed_target'])
        # print(time_start)
    else:
        U.printR('Get schedule failed')
        U.printR(response_1.text)
    
    time.sleep(25)

    response_2 = requests.get(Address_crawlback, headers=headers)
    if response_2.status_code == 200:
        Read_Json_2 = response_2.json()
        get_time_stamp = str(Read_Json_2['data'][-1]['timestamp'])
        get_amount     = str(Read_Json_2['data'][-1]['amount'])
        get_trigger    = str(Read_Json_2['data'][-1]['trigger'])
        # U.printY(f'Get time stamp  : {get_time_stamp}')
        # U.printY(f'Post time stamp : {Y}')
        check(get_time_stamp,"Time Stamp",f"{target_schedule}")
        check(get_amount,"Amount",feed_target)
        check(get_trigger,"Trigger","1")
        existence_check = all(find_res in list_res for find_res in find_res)
        if existence_check:
            feed_schedule_result.append("PASS")
            U.printG('=========== TEST FEEDING SCHEDULE DONE ============')
        else:
            U.printR('========== TEST FEEDING SCHEDULE FAILED ===========')
    else:
        U.printR('Request failed!')
        U.printR(response_2.text)
        U.printR('========== TEST FEEDING SCHEDULE FAILED ===========')

# Feeding_schedule(U.Address_Schedules,U.Address_Time,U.Address_crawlback)