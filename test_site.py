import requests
import Utility as U

test_site_result = []
list_res         = []
find_res         = ["ESP","ATG","PCB","RTC"]

def check(data, string, expect):
    if data == expect:
        U.printY(f"{string} : True   R: {data}  E: {expect}")
        list_res.append(string)
    else:
        U.printR(f"{string} : False  R: {data}  E: {expect}")

def Test_site(address, ESP_Version_E, ATG_Version_E, PCB_Version_E, RTC_Status_E):
    headers = U.headers()
    response = requests.get(address, headers=headers)
    U.printG('================== START TEST SITE  ===============')
    if response.status_code == 200:
        # U.printG('Request successful!')
        # print(response.json())
        Read_Json = response.json()
        ESP = Read_Json['wifi_version']
        ATG = Read_Json['versi']
        PCB = Read_Json['pcb_version']
        RTC = Read_Json['RTC_status']
        check(ESP,"ESP",ESP_Version_E)
        check(ATG,"ATG",ATG_Version_E)
        check(PCB,"PCB",PCB_Version_E)
        check(RTC,"RTC",RTC_Status_E)
        existence_check = all(find_res in list_res for find_res in find_res)
        if existence_check:
            test_site_result.append("PASS")
            U.printG("================== TEST SITE DONE =================")
        else:
            U.printR("================= TEST SITE FAILED ================")
    else:
        U.printR('Request failed!')
        U.printR(response.text)
        U.printR("================= TEST SITE FAILED ================")
        
# Test_site(U.Address_GetInfo, U.ESP_Version_E, U.ATG_Version_E, U.PCB_Version_E, U.RTC_Status_E)
