from colorama import Fore, Style
# TEMPORARY STORAGE
Percentage_Success = []
Percentage_Failed =[]

Address_Setting     = 'http://192.168.4.1:2516/setting'
Address_RSSI        = 'http://192.168.4.1:2516/scan_network'
Address_Current     = 'http://192.168.4.1:2516/current'
Address_GetInfo     = "http://192.168.4.1:2516/info?id=12484"
Address_Alert       = 'http://192.168.4.1:2516/alert'
Address_Schedules   = 'http://192.168.4.1:2516/schedules'
Address_Run         = 'http://192.168.4.1:2516/run'
Address_crawlback   = 'http://192.168.4.1:2516/get?page=1'
Address_Time        = 'http://192.168.4.1:2516/time'
Address_event       = 'http://192.168.4.1:2516/log?page=1'
TOKEN               = ''
SSID                = ''
PWM                 = []

# def val_txt(num):
#     with open("legacy.txt", "r") as target_file:
#         target = target_file.read()
#         line = target.splitlines()
#         raw = line[num].strip().split(':')
#         res = raw[-1].strip()
#         # print(f"token : {res}")
#     return res

def Target_SSID():
    global SSID
    res = SSID
    return res

def headers():
    global TOKEN
    headers = {
            'token': f'{TOKEN}'
        }
    return headers

# Header CSV
header_text_csv = [
        "DATE",
        "EQ CODE",
        "INSPECTOR",
        "POWER SWTICH",
        "LED INDICATOR",
        "TEST SITE",
        "THROWER DISTANCE",
        "EMPTY CURRENT",
        "RSSI LEVEL",
        "FEED SCHEDULE",
        "WDT FUNCTION",
        "RTC VOLTAGE",
        "BUTTON RUN",
        "BUTTON MENU",
        "BUTTON MINUS",
        "BUTTON PLUS",
        "BUTTON OK",
        "THROWER STALL",
        "DOSING STALL",
        "RESULT",
        "NOTE"
        ]

# COLORIZE STRING
def printG(Text):
    print(Fore.GREEN + f"{Text}"+ Fore.RESET)
def printY(Text):
    print(Fore.YELLOW + f"{Text}"+ Fore.RESET)
def printR(Text):
    print(Fore.RED + f"{Text}"+ Fore.RESET)
def printM(Text):
    print(Fore.MAGENTA + f"{Text}"+ Fore.RESET)
def printC(Text):
    print(Fore.CYAN + f"{Text}"+ Fore.RESET)
def printB(Text):
    print(Fore.BLUE + f"{Text}"+ Fore.RESET)
def printW(Text):
    print(Fore.WHITE + f"{Text}"+ Fore.RESET)
