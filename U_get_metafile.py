import requests
import Utility as U

headers = U.headers

def check(data, string, expect):
    if data == expect:
        U.printY(f"{string} : True   R: {data}  E: {expect}")
    else:
        U.printR(f"{string} : False  R: {data}  E: {expect}")

def get_metafile(address):
    U.printC('================== START TEST SITE  ===============')
    response = requests.get(address, headers=headers)
    if response.status_code == 200:
        print(response.json())
        Read_Json_2 = response.json()
        get_time_stamp = str(Read_Json_2['data'][-1]['timestamp'])
        get_amount     = str(Read_Json_2['data'][-1]['amount'])
        get_trigger    = str(Read_Json_2['data'][-1]['trigger'])
        U.printY(f'Get time stamp  : {get_time_stamp}')
        U.printG('=========== TEST FEEDING SCHEDULE DONE ============')
    else:
        U.printR(response.text)
        U.printR('========== TEST FEEDING SCHEDULE FAILED ===========')
        
get_metafile(U.Address_crawlback)
