from tkinter import *
from tkinter.ttk import *
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter.ttk import Progressbar
from tkinter import filedialog
from tkinter import Menu
import tkinter as tk
from tkinter import ttk

import System_check_report
import TerraPythonConfig
import Read_Write_Barak_Data_Base


MIN = 0
MAX = 250
main_window = Tk()
combo = Combobox(main_window)

def create_menu():
    menu = Menu(main_window)
    new_item = Menu(menu)
    new_item.add_command(label='New')
    new_item.add_separator()
    new_item.add_command(label='Edit')
    new_item.add_separator()
    new_item.add_command(label='Close')
    menu.add_cascade(label='File', menu=new_item)
    main_window.config(menu=menu)


def options_panel_create():
    class Checkbar(Frame):
        def __init__(self, parent=main_window, picks=[], side=LEFT, anchor=W):
            Frame.__init__(self, parent)
            self.vars = []
            for pick in picks:
                var = IntVar()
                chk = Checkbutton(self, text=pick, variable=var)
                chk.pack(side=side, anchor=anchor, expand=YES)
                self.vars.append(var)

        def state(self):
            return map((lambda var: var.get()), self.vars)

    root = Tk()
    lng = Checkbar(root, ['Clients Erorrs', 'servers status', 'Billing', 'Quota Update'])
    tgl = Checkbar(root, ['To File', 'Send To Server'])
    lng.pack(side=TOP, fill=X)
    tgl.pack(side=LEFT)
    #lng.config(relief=GROOVE, bd=2)

    def allstates():
        print(list(lng.state()), list(tgl.state()))#action run using the buttons

    Button(root, text='File', command=root.quit).pack(side=RIGHT)
    Button(root, text='Display', command=allstates).pack(side=RIGHT)
    root.mainloop()


def main():
    data_panel = tk.Tk()
    data_panel.title("SERVERS HEALTH STATUS - TERRA SAFE")
    main_window.title("Terra Safe - Barak Updater")
    main_window.attributes('-fullscreen', False)
    data_panel.attributes('-fullscreen',False)
    system_inf_text_rub = tk.Text(data_panel, height=100,width=100)
    S = tk.Scrollbar(data_panel)
    S.pack(side=tk.LEFT, fill=tk.Y)
    system_inf_text_rub.pack(side=tk.RIGHT, fill=tk.Y)
    S.config(command=system_inf_text_rub.yview)
    system_inf_text_rub.config(yscrollcommand=S.set)
    lbl = Label(main_window, text="barak data")
    lbl.grid(column=1, row=1)
    system_data_text = System_check_report.collectSystemInfo()
    create_menu()
    global manufacturer, computerType, display, location, user
    system_inf_text_rub.insert(tk.END,str(system_data_text))
    def updateBackupServer(event):
        backupServer = comboServer.get()
    #def updateComputerType(event):
     #   computerType = comboComputerType.get()
      #  data_record_dic.update({DATA_KEY_MACHINE_TYPE:computerType})
      #  print(computerType)
    #def updateDisplay(event):
       # display = comboDisplay.get()
       # data_record_dic.update({DATA_KEY_DISPLAY:display})
       # print(display)
   # def updateBuilding(event):
       # location = comboBuildings.get()
       # data_record_dic.update({DATA_KEY_LOCATION:location})
       # print(location)


    labelTop = tk.Label(main_window, text="Terra safe information")
    labelTop.grid(column=0, row=0)
    comboServer = ttk.Combobox(main_window, values=TerraPythonConfig.COMBOBOX_BACKUP_SERVER)
    comboServer.grid(column=0, row=1)
    comboServer.current(1)
    comboServer.bind("<<ComboboxSelected>>", updateBackupServer)

    userName = Entry(main_window, width=40)
    userName.grid(column=5, row=4)
    res = System_check_report.collectSystemInfo()
    show_db_files_bt_lbl = Label(main_window, text="system info spy")
    show_db_files_bt_lbl.configure(text=res)
    show_db_files = Button(main_window, text="SHOW DB FILES",
                 command=Read_Write_Barak_Data_Base.create_list_of_tables())
    show_db_files.grid(column=1, row=10)
    run_query_btn_lbl = Label(main_window, text="1")
    run_query_btn_lbl.configure(text=res)
    run_query_btn = Button(main_window, text="build", command=Read_Write_Barak_Data_Base.gui_start())
    run_query_btn.grid(column=1, row=11)
   # sn = SYSTEM_SPY.retriveSerialTagNumber()
    #text_view(10, 5, 0, 0,sn)
    options_panel_create()
    main_window.mainloop()


if __name__ == '__main__':
    main()

