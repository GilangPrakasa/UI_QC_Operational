import requests
import Utility as U
data = []
event_log_result = []
list_res         = []
find_res         = ['RUN_BUTTON_PRESSED','DISP_MENU_BUTTON_PRESSED','DISP_MINUS_BUTTON_PRESSED','DISP_PLUS_BUTTON_PRESSED','DISP_ENTER_BUTTON_PRESSED']

def check(value, list, x):
    global data
    if value in list:
        count = sum(1 for entry in x[0]["log"] if entry["event"] == value)
        U.printG(f"{value} true | count {count}")
        list_res.append(value)
    else:
        U.printR(f"{value} false")

def get_log(address):
    global data
    response = requests.get(address)
    U.printG('===================== CHECK LOG ===================')
    if response.status_code == 200:
        res = response.json()
        data.append(res)
        event_values = [entry["event"] for entry in data[0]["log"]]
        check('RUN_BUTTON_PRESSED',event_values,data)
        check('DISP_MENU_BUTTON_PRESSED',event_values,data)
        check('DISP_MINUS_BUTTON_PRESSED',event_values,data)
        check('DISP_PLUS_BUTTON_PRESSED',event_values,data)
        check('DISP_ENTER_BUTTON_PRESSED',event_values,data)
        data.clear()
        existence_check = all(find_res in list_res for find_res in find_res)
        if existence_check:
            event_log_result.append("PASS")
            U.printG('================== CHECK LOG DONE =================')
        else:
            U.printR('================= CHECK LOG FAILED ================')
    else:
        U.printR('Request failed!')
        U.printR(response.text)
        U.printR('================= CHECK LOG FAILED ================')
        
# get_log(U.Address_event)
