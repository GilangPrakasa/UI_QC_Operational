# IMPORT
import test_site            as TS
import thrower_distance     as TD
import read_current         as RC
import rssi_level           as RL
import feeding_schedule     as FS
import wdt_function         as WF
import get_event_log        as LOG
import test_stall           as TSL
import Utility              as U

from CTkMessagebox import CTkMessagebox
from datetime import datetime
import customtkinter, sys, re, csv, time, os.path

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')

# DUMMY ADDRESS
address_setting     = ''
address_RSSI        = ''
address_current     = ''
address_get_info    = ''
address_alert       = ''
address_schedules   = ''
address_run         = ''
address_crawlback   = ''
address_time        = ''
address_event       = ''
token               = ''

# DUMMY DATA
MODE    = ""
IDC     = ""
TKN     = ""
FWR     = ""
ATG     = ""
PCB     = ""
RTC     = ""
SSID    = ""
data    = ""

class StdoutRedirector:
    def __init__(self, filename=None):
        self.terminal = sys.stdout
        self.filename = filename or "log/dump.txt"
        self.log = open(self.filename, "a")

    def update_filename(self, new_filename):
        self.filename = new_filename
        self.log.close()
        self.log = open(self.filename, "a")

    def write(self, message):
        global data
        data = ansi_escape.sub('', message)
        self.terminal.write(message)
        self.log.write(data)
        self.log.flush()
        os.fsync(self.log.fileno())

    def flush(self):
        pass

    # def __init__(self):
    #     self.terminal = sys.stdout
    #     # self.textbox = textbox
    #     self.log = open("dump.txt", "a")

    # def write(self, message):
    #     global data
    #     data = ansi_escape.sub('', message)
    #     self.terminal.write(message)
    #     self.log.write(data) 
    #     # self.textbox.insert("end", data)
    #     # self.textbox.see("end")  # Scroll to the end

    # def flush(self):
    #     pass 

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        sys.stdout = StdoutRedirector()
        self.title("QC OPERATIONAL")
        self.iconbitmap('assets/iconx.ico')

        # configure grid layout
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)

        # FRAME 1
        self.FR1 = customtkinter.CTkFrame(self, width=200, corner_radius=0, border_width=0)
        self.FR1.grid(row=0, column=3, rowspan=4, sticky="nsew")
        self.FR1.grid_rowconfigure(10, weight=1)

        self.label = customtkinter.CTkLabel(self.FR1, text="SETTING", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.label.grid(row=0, column=0, padx=10, pady=10)

        self.btn_load = customtkinter.CTkButton(self.FR1, width=200, text="LOAD SETTING", command=load_setting)
        self.btn_load.grid(row=1, column=0, padx=10, pady=10)
        
        self.load_value = customtkinter.CTkTextbox(self.FR1, width=200, height=185)
        self.load_value.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        # self.input_setting.configure(state="disabled")

        self.btn_text = customtkinter.StringVar()
        self.inspector_btn = customtkinter.CTkButton(self.FR1, width=200, textvariable=self.btn_text, command=set_inspector)
        self.inspector_btn.grid(row=3, column=0, padx=10, pady=10)
        self.btn_text.set("Set Inspector")
        
        self.mode_execute = customtkinter.CTkOptionMenu(self.FR1, width=200, values=["MODE AP", "MODE SA"], command=optionmenu_callback)
        self.mode_execute.grid(row=4, column=0, padx=10, pady=10)
        self.mode_execute.set("MODE")

        self.eq_var = customtkinter.CTkEntry(self.FR1, width=200, placeholder_text="EQ CODE")
        self.eq_var.grid(row=5, column=0, padx=10, pady=10)

        self.exe_btn = customtkinter.CTkButton(self.FR1, width=200, text="EXECUTE", command=handling_mode)
        self.exe_btn.grid(row=6, column=0, padx=10, pady=10)
        self.exe_btn.configure(fg_color="green")

        self.label = customtkinter.CTkLabel(self.FR1, text="mahesa.gilang@efishery.com", font=customtkinter.CTkFont(size=15))
        self.label.grid(row=7, column=0, padx=0, pady=0)

        # self.stop_btn = customtkinter.CTkButton(self.FR1, width=50, text="DEBUG", command=button_click)
        # self.stop_btn.grid(row=7, column=0, padx=10, pady=10)

        # FRAME 2
        self.FR2 = customtkinter.CTkFrame(self, width=0, corner_radius=0, border_width=0)
        self.FR2.grid(row=0, column=2, rowspan=4, sticky="nsew")
        self.FR2.grid_rowconfigure(10, weight=1)

        self.label = customtkinter.CTkLabel(self.FR2, text="MONITORING", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.label.grid(row=0, column=0, padx=10, pady=10)

        self.monitoring = customtkinter.CTkTextbox(self.FR2, width=200, height=377)
        self.monitoring.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        # sys.stdout = StdoutRedirector(self.monitoring)

        self.clear_btn = customtkinter.CTkButton(self.FR2, width=200, text="CLEAR", command=clear_text_box)
        self.clear_btn.grid(row=2, column=0, padx=10, pady=10)

        # FRAME 3
        self.FR3 = customtkinter.CTkFrame(self, width=0, corner_radius=0, border_width=0)
        self.FR3.grid(row=0, column=1, rowspan=4, sticky="nsew")
        self.FR3.grid_rowconfigure(10, weight=1)

        self.label = customtkinter.CTkLabel(self.FR3, text="AUTOMATE TEST", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.label.grid(row=0, column=0, padx=10, pady=10)

        self.btn_1 = customtkinter.CTkButton(self.FR3, width=130, corner_radius=20, text="TEST SITE", command=test_site)
        self.btn_1.grid(row=1, column=0, padx=10, pady=10)
        self.btn_1.configure(fg_color="green")
        
        self.btn_2 = customtkinter.CTkButton(self.FR3, width=130, corner_radius=20, text="EMPTY CURRENT", command=read_current)
        self.btn_2.grid(row=2, column=0, padx=10, pady=10)
        self.btn_2.configure(fg_color="green")

        self.btn_3 = customtkinter.CTkButton(self.FR3, width=130, corner_radius=20, text="THROWER PWM", command=thrower_distance)
        self.btn_3.grid(row=3, column=0, padx=10, pady=10)
        self.btn_3.configure(fg_color="green")
        
        self.btn_4 = customtkinter.CTkButton(self.FR3, width=130, corner_radius=20, text="RSSI LEVEL", command=rssi_level)
        self.btn_4.grid(row=4, column=0, padx=10, pady=10)
        self.btn_4.configure(fg_color="green")
        
        self.btn_5 = customtkinter.CTkButton(self.FR3, width=130, corner_radius=20, text="FEED SCHEDULE", command=feed_schedule)
        self.btn_5.grid(row=5, column=0, padx=10, pady=10)
        self.btn_5.configure(fg_color="green")
        
        self.btn_6 = customtkinter.CTkButton(self.FR3, width=130, corner_radius=20, text="WDT FUNCTION", command=wdt_function)
        self.btn_6.grid(row=6, column=0, padx=10, pady=10)
        self.btn_6.configure(fg_color="green")

        self.btn_7 = customtkinter.CTkButton(self.FR3, width=130, corner_radius=20, text="CHECK LOG", command=get_log)
        self.btn_7.grid(row=7, column=0, padx=10, pady=10)
        self.btn_7.configure(fg_color="green")

        self.btn_8 = customtkinter.CTkButton(self.FR3, width=130, corner_radius=20, text="STALL PREP", command=test_stall)
        self.btn_8.grid(row=8, column=0, padx=10, pady=10)
        self.btn_8.configure(fg_color="green")

        self.save_btn = customtkinter.CTkButton(self.FR3, width=130, corner_radius=20, text="SAVE", command=save_result)
        self.save_btn.grid(row=9, column=0, padx=10, pady=10)

        self.orig_color = self.save_btn.cget("fg_color")

        # FRAME 4
        self.FR4 = customtkinter.CTkFrame(self, width=200, corner_radius=0, border_width=0)
        self.FR4.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.FR4.grid_rowconfigure(13, weight=1)
        self.FR4.grid_columnconfigure(3, weight=1)

        self.label = customtkinter.CTkLabel(self.FR4, text="SCOPE TEST", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.switch_var = customtkinter.StringVar(value="FAIL")
        self.switch_var = customtkinter.CTkCheckBox(self.FR4, text="POWER SWITCH", variable=self.switch_var, onvalue="PASS", offvalue="FAIL")
        self.switch_var.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.led_var = customtkinter.StringVar(value="FAIL")
        self.led_var = customtkinter.CTkCheckBox(self.FR4, text="LED INDICATOR", variable=self.led_var, onvalue="PASS", offvalue="FAIL")
        self.led_var.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.test_site_var = customtkinter.StringVar(value="FAIL")
        self.test_site_var = customtkinter.CTkCheckBox(self.FR4, text="TEST SITE", variable=self.test_site_var, onvalue="PASS", offvalue="FAIL")
        self.test_site_var.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        self.empty_current_var = customtkinter.StringVar(value="FAIL")
        self.empty_current_var = customtkinter.CTkCheckBox(self.FR4, text="EMPTY CURRENT", variable=self.empty_current_var, onvalue="PASS", offvalue="FAIL")
        self.empty_current_var.grid(row=4, column=0, padx=10, pady=10, sticky="w")

        self.pwm_var = customtkinter.StringVar(value="FAIL")
        self.pwm_var = customtkinter.CTkCheckBox(self.FR4, text="THROWER PWM", variable=self.pwm_var, onvalue="PASS", offvalue="FAIL")
        self.pwm_var.grid(row=5, column=0, padx=10, pady=10, sticky="w")

        self.rssi_var = customtkinter.StringVar(value="FAIL")
        self.rssi_var = customtkinter.CTkCheckBox(self.FR4, text="RSSI LEVEL", variable=self.rssi_var, onvalue="PASS", offvalue="FAIL")
        self.rssi_var.grid(row=6, column=0, padx=10, pady=10, sticky="w")

        self.schedule_var = customtkinter.StringVar(value="FAIL")
        self.schedule_var = customtkinter.CTkCheckBox(self.FR4, text="SCHEDULE", variable=self.schedule_var, onvalue="PASS", offvalue="FAIL")
        self.schedule_var.grid(row=7, column=0, padx=10, pady=10, sticky="w")

        self.wdt_var = customtkinter.StringVar(value="FAIL")
        self.wdt_var = customtkinter.CTkCheckBox(self.FR4, text="WDT FUNCTION", variable=self.wdt_var, onvalue="PASS", offvalue="FAIL")
        self.wdt_var.grid(row=8, column=0, padx=10, pady=10, sticky="w")

        self.rtc_var = customtkinter.StringVar(value="FAIL")
        self.rtc_var = customtkinter.CTkCheckBox(self.FR4, text="RTC > 3.1V", variable=self.rtc_var, onvalue="PASS", offvalue="FAIL")
        self.rtc_var.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        self.btn_run_var = customtkinter.StringVar(value="FAIL")
        self.btn_run_var = customtkinter.CTkCheckBox(self.FR4, text="BUTTON RUN", variable=self.btn_run_var, onvalue="PASS", offvalue="FAIL")
        self.btn_run_var.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        self.btn_menu_var = customtkinter.StringVar(value="FAIL")
        self.btn_menu_var = customtkinter.CTkCheckBox(self.FR4, text="BUTTON MENU", variable=self.btn_menu_var, onvalue="PASS", offvalue="FAIL")
        self.btn_menu_var.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        self.btn_minus_var = customtkinter.StringVar(value="FAIL")
        self.btn_minus_var = customtkinter.CTkCheckBox(self.FR4, text="BUTTON MINUS", variable=self.btn_minus_var, onvalue="PASS", offvalue="FAIL")
        self.btn_minus_var.grid(row=4, column=1, padx=10, pady=10, sticky="w")

        self.btn_plus_var = customtkinter.StringVar(value="FAIL")
        self.btn_plus_var = customtkinter.CTkCheckBox(self.FR4, text="BUTTON PLUS", variable=self.btn_plus_var, onvalue="PASS", offvalue="FAIL")
        self.btn_plus_var.grid(row=5, column=1, padx=10, pady=10, sticky="w")

        self.btn_ok_var = customtkinter.StringVar(value="FAIL")
        self.btn_ok_var = customtkinter.CTkCheckBox(self.FR4, text="BUTTON OK", variable=self.btn_ok_var, onvalue="PASS", offvalue="FAIL")
        self.btn_ok_var.grid(row=6, column=1, padx=10, pady=10, sticky="w")

        self.thrower_var = customtkinter.StringVar(value="FAIL")
        self.thrower_var = customtkinter.CTkCheckBox(self.FR4, text="THROWER STALL", variable=self.thrower_var, onvalue="PASS", offvalue="FAIL")
        self.thrower_var.grid(row=7, column=1, padx=10, pady=10, sticky="w")

        self.dosing_var = customtkinter.StringVar(value="FAIL")
        self.dosing_var = customtkinter.CTkCheckBox(self.FR4, text="DOSING STALL", variable=self.dosing_var, onvalue="PASS", offvalue="FAIL")
        self.dosing_var.grid(row=8, column=1, padx=10, pady=10, sticky="w")

        self.label = customtkinter.CTkLabel(self.FR4, text="RESULT                  :", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.label.grid(row=9, column=0, padx=10, pady=10, sticky="W")
        
        self.res_var = customtkinter.CTkOptionMenu(self.FR4, width=150, values=["FAIL", "PASS", "PASS /w NOTE"])
        self.res_var.grid(row=9, column=1, padx=10, pady=10, sticky="W")
        self.res_var.set("RESULT")

        self.label = customtkinter.CTkLabel(self.FR4, text="NOTE                     :", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.label.grid(row=10, column=0, padx=10, pady=10, sticky="W")

        self.NOTE = customtkinter.CTkEntry(self.FR4, width=150, placeholder_text="NOTE")
        self.NOTE.grid(row=10, column=1, padx=10, pady=10, sticky="W")

        # self.save_btn = customtkinter.CTkButton(self.FR4, width=180, corner_radius=20, text="SAVE", command=save_result)
        # self.save_btn.grid(row=11, column=0, columnspan=2, padx=10, pady=10)

def button_click():
    global MODE,IDC,TKN,FWR,ATG,PCB,RTC,SSID
    # print(f"TS  {TS.test_site_result}")
    # print(f"TD  {TD.thrower_pwm_result}")
    # print(f"RC  {RC.read_current_result}")
    # print(f"RL  {RL.rssi_level_result}")
    # print(f"FS  {FS.feed_schedule_result}")
    # print(f"WF  {WF.wdt_function_result}")
    # print(f"LOG {LOG.event_log_result}")
    # print(f"STL {TSL.prep_stall_result}")
    print(IDC ) 
    print(TKN ) 
    print(FWR ) 
    print(ATG ) 
    print(PCB ) 
    print(RTC ) 
    print(SSID) 
    print(" ")
    print(U.TOKEN)
    print(U.SSID)
    print(U.PWM)

def clear_text_box():
    global MODE,IDC,TKN,FWR,ATG,PCB,RTC,SSID
    app.monitoring.delete(0.0,"end")
    TS.test_site_result.clear()
    TD.thrower_pwm_result.clear()
    RC.read_current_result.clear()
    RL.rssi_level_result.clear()
    FS.feed_schedule_result.clear()
    WF.wdt_function_result.clear()
    LOG.event_log_result.clear()
    TSL.prep_stall_result.clear()

    app.exe_btn.configure(fg_color="red")
    IDC  = ''
    TKN  = ''
    FWR  = ''
    ATG  = ''
    PCB  = ''
    RTC  = ''
    SSID = ''
    U.TOKEN = ''
    U.SSID  = ''
    U.PWM.clear()
    U.printR("********************** CLEAR **********************")
   
def save_result():
    global start_time
    data_text = [
        f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
        f"{app.eq_var.get()}",
        f"{app.user_input}",
        f"{app.switch_var.get()}",
        f"{app.led_var.get()}",
        f"{app.test_site_var.get()}",
        f"{app.pwm_var.get()}",
        f"{app.empty_current_var.get()}",
        f"{app.rssi_var.get()}",
        f"{app.schedule_var.get()}",
        f"{app.wdt_var.get()}",
        f"{app.rtc_var.get()}",
        f"{app.btn_run_var.get()}",
        f"{app.btn_menu_var.get()}",
        f"{app.btn_minus_var.get()}",
        f"{app.btn_plus_var.get()}",
        f"{app.btn_ok_var.get()}",
        f"{app.thrower_var.get()}",
        f"{app.dosing_var.get()}",
        f"{app.res_var.get()}",
        f"{app.NOTE.get()}"
        ]
    state_empty = ""
    if state_empty in data_text:
        CTkMessagebox(title="Message",width=150,height=100,message="Something is empty",icon="assets/icon.png", option_1="ok")
    else: 
        header_text = U.header_text_csv
        date_now = datetime.now().strftime("%d.%m.%Y")
        date_month = datetime.now().strftime("%m.%Y")
        check_file = os.path.isfile(f"{date_month}.csv")
        csv_file_path = f"{date_month}.csv"
        if check_file == False:
            with open(csv_file_path, mode='a', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(header_text)

        with open(csv_file_path, mode='a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(data_text)
            end_time = time.time()
            elapsed_time = end_time - start_time
            stopwatch = "Elapsed time: {:.2f} minute".format(elapsed_time/60)
            U.printM(f"DATA SAVE {app.eq_var.get()}")
            U.printM(stopwatch)
            U.printM("******************** ENDED QC  ********************")
            U.printW("")
            app.eq_var.delete(0,20)
            app.switch_var.deselect()
            app.led_var.deselect()
            app.test_site_var.deselect()
            app.pwm_var.deselect()
            app.empty_current_var.deselect()
            app.rssi_var.deselect()
            app.schedule_var.deselect()
            app.wdt_var.deselect()
            app.rtc_var.deselect()
            app.btn_run_var.deselect()
            app.btn_menu_var.deselect()
            app.btn_minus_var.deselect()
            app.btn_plus_var.deselect()
            app.btn_ok_var.deselect()
            app.thrower_var.deselect()
            app.dosing_var.deselect()
            app.res_var.set("RESULT")
            app.NOTE.delete(0,20)
            app.exe_btn.configure(fg_color="red")
            app.btn_1.configure(fg_color="red")
            app.btn_2.configure(fg_color="red")
            app.btn_3.configure(fg_color="red")
            app.btn_4.configure(fg_color="red")
            app.btn_5.configure(fg_color="red")
            app.btn_6.configure(fg_color="red")
            app.btn_7.configure(fg_color="red")
            app.btn_8.configure(fg_color="red")
            # clear_text_box()
            app.monitoring.insert("end", f"{stopwatch}\n")

def address_SA():
    global address_setting,address_RSSI,address_current,address_get_info,address_alert,address_schedules,address_run,address_crawlback,address_time, address_event     
    address_setting     = 'http://192.168.4.1:2516/setting'
    address_RSSI        = 'http://192.168.4.1:2516/scan_network'
    address_current     = 'http://192.168.4.1:2516/current'
    address_get_info    = 'http://192.168.4.1:2516/info?id=12484'
    address_alert       = 'http://192.168.4.1:2516/alert'
    address_schedules   = 'http://192.168.4.1:2516/schedules'
    address_run         = 'http://192.168.4.1:2516/run'
    address_crawlback   = 'http://192.168.4.1:2516/get?page=1'
    address_time        = 'http://192.168.4.1:2516/time'
    address_event       = 'http://192.168.4.1:2516/log?page=1'

def address_AP(ID_COBOX):
    global address_setting,address_RSSI,address_current,address_get_info,address_alert,address_schedules,address_run,address_crawlback,address_time, address_event 
    address_setting     = f'http://efishery_{ID_COBOX}.local:2516/setting'
    address_RSSI        = f'http://efishery_{ID_COBOX}.local:2516/scan_network'
    address_current     = f'http://efishery_{ID_COBOX}.local:2516/current'
    address_get_info    = f'http://efishery_{ID_COBOX}.local:2516/info?id=12484'
    address_alert       = f'http://efishery_{ID_COBOX}.local:2516/alert'
    address_schedules   = f'http://efishery_{ID_COBOX}.local:2516/schedules'
    address_run         = f'http://efishery_{ID_COBOX}.local:2516/run'
    address_crawlback   = f'http://efishery_{ID_COBOX}.local:2516/get?page=1'
    address_time        = f'http://efishery_{ID_COBOX}.local:2516/time'
    address_event       = f'http://efishery_{ID_COBOX}.local:2516/log?page=1'

def set_inspector():
    dialog = customtkinter.CTkInputDialog(text="Siapa anda ?", title="Set Inspector")
    app.user_input = dialog.get_input()
    app.btn_text.set(f"{app.user_input}")

def load_setting():
    global MODE,IDC,TKN,FWR,ATG,PCB,RTC,SSID
    file_path = customtkinter.filedialog.askopenfilename(title="Select a text file")
    if file_path:
        with open(file_path, 'r') as file:
            content = file.read()
            app.load_value.delete(0.0,"end") 
            app.load_value.insert(0.0,content)
            # IDC  = handling_setting(0)
            # TKN  = handling_setting(1)
            # FWR  = handling_setting(2)
            # ATG  = handling_setting(3)
            # PCB  = handling_setting(4)
            # RTC  = handling_setting(5)
            # SSID = handling_setting(6)

def handling_setting(num):
    try:
        content = app.load_value.get("1.0", "end-1c")
        line = content.splitlines()
        raw = line[num].strip().split(':')
        res = str(raw[-1].strip())
        return res
    except Exception as e:
        CTkMessagebox(title="Message",width=150,height=100,message="Do input setting",icon="assets/icon.png",option_1="ok")

def handling_mode():
    global MODE,IDC,TKN,FWR,ATG,PCB,RTC,SSID,start_time
    date = datetime.now().strftime("%d-%m-%Y")
    timestamp = datetime.now().strftime("%H:%M:%S")
    content = app.load_value.get("1.0", "end-1c").splitlines()
    if len(content) >= 7:
        IDC  = handling_setting(0)
        TKN  = handling_setting(1)
        FWR  = handling_setting(2)
        ATG  = handling_setting(3)
        PCB  = handling_setting(4)
        RTC  = handling_setting(5)
        SSID = handling_setting(6)
        PWM  = handling_setting(7).split(",")
        U.TOKEN = TKN
        U.SSID  = SSID
        U.PWM = [int(value) for value in PWM]
        code = app.eq_var.get()
        sys.stdout.update_filename(f"log/{date}-{code}.txt")
        if hasattr(app, 'user_input'):
            pass
        else:
            CTkMessagebox(title="Message",width=150,height=100,message="Please input inspector",icon="assets/icon.png",option_1="ok")
        if MODE == "MODE AP":
            if len(code) >= 5 and app.user_input is not None and len(app.user_input) >= 1:
                U.printM(f"****{date}***** STARTING QC ******{timestamp}*****")
                U.printM(f"{MODE}, INSPECTOR = {app.user_input}, EQ CODE = {code}")
                app.monitoring.insert("end", f"{MODE}/{app.user_input}/{code}\n")
                app.exe_btn.configure(fg_color="green")
                start_time = time.time()
            else:
                CTkMessagebox(title="Message",width=150,height=100,message="Something is empty",icon="assets/icon.png",option_1="ok")
        if MODE == "MODE SA":
            if len(code) >= 5 and app.user_input is not None and len(app.user_input) >= 1:
                address_SA()
                U.printM(f"****{date}***** STARTING QC ******{timestamp}*****")
                U.printM(f"{MODE}, INSPECTOR = {app.user_input}, EQ CODE = {code}")
                app.monitoring.insert("end", f"{MODE}/{app.user_input}/{code}\n")
                app.exe_btn.configure(fg_color="green")
                start_time = time.time()
            else:
                CTkMessagebox(title="Message",width=150,height=100,message="Something is empty",icon="assets/icon.png",option_1="ok")
        else:
              CTkMessagebox(title="Message",width=150,height=100,message="Choose mode please",icon="assets/icon.png",option_1="ok")
    else:
        CTkMessagebox(title="Message",width=150,height=100,message="Do input setting",icon="assets/icon.png",option_1="ok")

def optionmenu_callback(choice):
    global MODE
    MODE = choice

def test_site():
    try:
        TS.Test_site(address_get_info,FWR,ATG,PCB,RTC)
        if len(TS.test_site_result) == 1:
            app.btn_1.configure(fg_color="green")
            app.test_site_var.select()
            print("TEST SITE SUCCESS")
            app.monitoring.insert("end", "TEST SITE SUCCESS\n")
        else:
            app.btn_1.configure(fg_color="yellow")
    except Exception as e:
        app.btn_1.configure(fg_color="yellow")
        CTkMessagebox(title="Message",width=150,height=100,message="Something error",icon="assets/icon.png",option_1="ok")

def thrower_distance():
    try:
        TD.thrower_pwm(address_setting,address_run,address_current)
        if len(TD.thrower_pwm_result) == 1:
            app.btn_3.configure(fg_color="green")
            app.pwm_var.select()
            print("THROWER DISTANCE SUCCESS")
            app.monitoring.insert("end", "THROWER PWM SUCCESS\n")
        else:
            app.btn_3.configure(fg_color="yellow")
    except Exception as e:
        app.btn_3.configure(fg_color="yellow")
        CTkMessagebox(title="Message",width=150,height=100,message="Something error",icon="assets/icon.png",option_1="ok")

def read_current():
    try:
        RC.Read_Current(address_current,address_run)
        if len(RC.read_current_result) == 1:
            app.btn_2.configure(fg_color="green")
            app.empty_current_var.select()
            print("READ CURRENT SUCCESS")
            app.monitoring.insert("end", "READ CURRENT SUCCESS\n")
        else:
            app.btn_2.configure(fg_color="yellow")
    except Exception as e:
        app.btn_2.configure(fg_color="yellow")
        CTkMessagebox(title="Message",width=150,height=100,message="Something error",icon="assets/icon.png",option_1="ok")

def rssi_level():
    try:
        RL.RSSI_Level(address_RSSI)
        if len(RL.rssi_level_result) == 1:
            app.btn_4.configure(fg_color="green")
            app.rssi_var.select()
            print("RSSI LEVEL SUCCESS")
            app.monitoring.insert("end", "RSSI LEVEL SUCCESS\n")
        else:
            app.btn_4.configure(fg_color="yellow")
    except Exception as e:
        app.btn_4.configure(fg_color="yellow")
        CTkMessagebox(title="Message",width=150,height=100,message="Something error",icon="assets/icon.png",option_1="ok")

def feed_schedule():
    try:
        FS.Feeding_schedule(address_schedules,address_time,address_crawlback)
        if len(FS.feed_schedule_result) == 1:
            app.btn_5.configure(fg_color="green")
            app.schedule_var.select()
            print("FEED SCHEDULE SUCCESS")
            app.monitoring.insert("end", "FEED SCHEDULE SUCCESS\n")
        else:
            app.btn_5.configure(fg_color="yellow")
    except Exception as e:
        app.btn_5.configure(fg_color="yellow")
        CTkMessagebox(title="Message",width=150,height=100,message="Something error",icon="assets/icon.png",option_1="ok")

def wdt_function():
    try:
        CTkMessagebox(width=150,height=100,message="PLEASE RECONNECT WIFI AFTER RESTARTING",icon="assets/icon.png",option_1="ok")
        WF.Simulate_hang(address_alert,address_run)
        if len(WF.wdt_function_result) == 1:
            app.btn_6.configure(fg_color="green")
            app.wdt_var.select()
            print("WDT FUNCTION SUCCESS")
            app.monitoring.insert("end", "WDT FUNCTION SUCCESS\n")
        else:
            app.btn_6.configure(fg_color="yellow") 
    except Exception as e:
        app.btn_6.configure(fg_color="yellow") 
        CTkMessagebox(title="Message",width=150,height=100,message="Something error",icon="assets/icon.png",option_1="ok")

def get_log():
    try:
        LOG.get_log(address_event)
        if len(LOG.event_log_result) == 1:
            app.btn_7.configure(fg_color="green")
            app.btn_run_var.select()
            app.btn_menu_var.select()
            app.btn_minus_var.select()
            app.btn_plus_var.select()
            app.btn_ok_var.select()
            print("EVENT LOG SUCCESS")
            app.monitoring.insert("end", "EVENT LOG SUCCESS\n")
        else:
            app.btn_7.configure(fg_color="yellow")
    except Exception as e:
        app.btn_7.configure(fg_color="yellow")
        CTkMessagebox(title="Message",width=150,height=100,message="Something error",icon="assets/icon.png",option_1="ok")

def test_stall():
    try:
        TSL.Run_Stall(address_run,address_current)
        if len(TSL.prep_stall_result) == 1:
            app.btn_8.configure(fg_color="green")
            app.monitoring.insert("end", "PREPARE STALL SUCCESS\n")
        else:
            app.btn_8.configure(fg_color="yellow")
    except Exception as e:
        app.btn_8.configure(fg_color="yellow")
        CTkMessagebox(title="Message",width=150,height=100,message="Something error",icon="assets/icon.png",option_1="ok")

if __name__ == "__main__":
    app = App()
    app.mainloop()
    