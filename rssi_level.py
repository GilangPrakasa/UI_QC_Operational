from bs4 import BeautifulSoup
from urllib import request
import Utility as U
 
rssi_level_result = []

def RSSI_Level(Address_RSSI):
    Target_SSID = U.Target_SSID()
    response = request.urlopen(Address_RSSI)
    U.printG('============== START TEST RSSI LEVEL ==============')
    html_content = response.read()
    Get_data_Html = BeautifulSoup(html_content, 'html.parser')
    Get_string = str(Get_data_Html).split("<br/>")
    SSID_line = [line for line in Get_string if Target_SSID in line]
    # print(SSID_line)
    if SSID_line:
        modified_line = ' '.join(SSID_line[0].split()[1:])
        # print(modified_line)
        start_index = modified_line.find('-')
        dbm_value = modified_line[start_index:modified_line.find('dBm')].strip()
        # print(dbm_value)
        RSSI = float(dbm_value)
        # print(RSSI)
        if RSSI >= -70:
            U.printY(f"{modified_line}    >= -70 dBm")
            U.printG("============ RSSI LEVEL TEST SUCCESS ! ============")
            rssi_level_result.append("PASS")
        else:
            U.printY(f"{modified_line}    <= -70 dBm")
            U.printR("============ RSSI_Level TEST FAILED !! ============")
            U.Percentage_Failed.append("RSSI LEVEL")
    else:
        U.printR('================ SSID NOT FOUND !! ================')
        U.printR('============ PLEASE CHECK ACCESS POINT ============')

# RSSI_Level(U.Address_RSSI)

    # U.printW(' ')
    # U.printC('============== START TEST RSSI LEVEL ==============')
    # response = request.urlopen(Address_RSSI)
    # html_content = response.read()
    # Get_data_Html = BeautifulSoup(html_content, 'html.parser')
    # Get_string = str(Get_data_Html).split("<br/>")
    # # print(Get_string)
    # modified_line = ' '.join(Get_string)
    # # print(modified_line)
    # RSSI_Level = float(modified_line)
    # if RSSI_Level > -70:
    #     U.printY(f"{modified_line} > -70 dBm")
    #     U.printG("============ RSSI LEVEL TEST SUCCESS ! ============")
    #     U.Percentage_Success.append("RSSI LEVEL")
    # else:
    #     U.printY(f"{modified_line} < -70 dBm")
    #     U.printR("============ RSSI_Level TEST FAILED !! ============")
    #     U.Percentage_Failed.append("RSSI LEVEL")

