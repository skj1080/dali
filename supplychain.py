# -*- coding: utf-8 -*-
import operator
import os
import glob
import shutil
import time
import pickle
import datetime
import json
from tkinter import *
from tkinter.font import *
from demo.demo_smartcontract import smart_contract
from demo.demo_smartcontract import run_smartcontract
from demo.demo_smartcontract import request_test
node_info = {"163.239.195.133" : "House A","163.239.195.120" : "Okchun Hub Center"}
def isNumber(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

class contract_GUI:
    def __init__(self, parent):
        global contents_list
        global Date
        global ID
        self.myParent = parent
        contents_list = []
        Date = 0
        ID = ""
        # Title -----------------
        fontObject1 = Font(self.myParent, family='Times New Roman', size=15, weight='bold')
        sysTitle = Label(self.myParent, text='Safe Transfer System')
        sysTitle['font'] = fontObject1
        sysTitle.place(x=50, y=0, width=210, height=50)

        sysTitle = Label(self.myParent, text='Constraints & Text')
        sysTitle['font'] = fontObject1
        sysTitle.place(x=395, y=0, width=210, height=50)

        # input ----------
        fontObject2 = Font(self.myParent, family='Times New Roman', size=10)

        IP_text = Label(self.myParent, text='Deploy IP')
        IP_text['font'] = fontObject2
        IP_text.place(x=0, y=50, width=115, height=30)

        self.IP_input = Entry(self.myParent)
        self.IP_input.configure(font=fontObject2)
        self.IP_input.place(x=30, y=80, width=240, height=20)

        ID_text = Label(self.myParent, text='Device ID')
        ID_text['font'] = fontObject2
        ID_text.place(x=0, y=110, width=115, height=30)

        self.ID_input = Entry(self.myParent)
        self.ID_input.configure(font=fontObject2)
        self.ID_input.place(x=30, y=140, width=240, height=20)

        Contents_text = Label(self.myParent, text='Add New Contents')
        Contents_text['font'] = fontObject2
        Contents_text.place(x=0, y=170, width=160, height=30)

        self.Contents_input = Entry(self.myParent)
        self.Contents_input.configure(font=fontObject2)
        self.Contents_input.place(x=30, y=200, width=240, height=20)

        Value_text = Label(self.myParent, text='Safe Value (Upper Bound)')
        Value_text['font'] = fontObject2
        Value_text.place(x=0, y=230, width=190, height=30)

        self.Value_input = Entry(self.myParent)
        self.Value_input.configure(font=fontObject2)
        self.Value_input.place(x=30, y=260, width=240, height=20)

        Value2_text = Label(self.myParent, text='Safe Value (Lower Bound)')
        Value2_text['font'] = fontObject2
        Value2_text.place(x=0, y=290, width=190, height=30)

        self.Value2_input = Entry(self.myParent)
        self.Value2_input.configure(font=fontObject2)
        self.Value2_input.place(x=30, y=320, width=240, height=20)

        Time_text = Label(self.myParent, text='Excess Timeout (min)')
        Time_text['font'] = fontObject2
        Time_text.place(x=0, y=350, width=175, height=30)

        self.Time_input = Entry(self.myParent)
        self.Time_input.configure(font=fontObject2)
        self.Time_input.place(x=30, y=380, width=240, height=20)

        Date_text = Label(self.myParent, text='Goal Date  ex)2018-05-10 18:30:00              \n (if it doesn\'t matter, write 0 )')
        Date_text['font'] = fontObject2
        Date_text.place(x=0, y=410, width=280, height=30)

        self.Date_input = Entry(self.myParent)
        self.Date_input.configure(font=fontObject2)
        self.Date_input.place(x=30, y=440, width=240, height=20)

        self.submit_button = Button(self.myParent,
                                      command=self.button1Click)
        self.submit_button.bind("<Return>", self.button1Click)
        self.submit_button.configure(text="Submit", background="gray")
        self.submit_button.place(x=465, y=560, width=70, height=30)

        self.Add_button = Button(self.myParent,
                                      command=self.button3Click)
        self.Add_button.bind("<Return>", self.button3Click)
        self.Add_button.configure(text="Add", background="gray")
        self.Add_button.place(x=110, y=470, width=70, height=30)

        Date_text = Label(self.myParent, text='Contract Address')
        Date_text['font'] = fontObject2
        Date_text.place(x=0, y=500, width=160, height=30)

        self.Address_input = Entry(self.myParent)
        self.Address_input.configure(font=fontObject2)
        self.Address_input.place(x=30, y=530, width=240, height=20)

        self.check_button = Button(self.myParent,
                                      command=self.button2Click)
        self.check_button.bind("<Return>", self.button2Click)
        self.check_button.configure(text="Check", background="gray")
        self.check_button.place(x=70, y=560, width=70, height=30)

        self.loc_button = Button(self.myParent,
                                      command=self.button4Click)
        self.loc_button.bind("<Return>", self.button4Click)
        self.loc_button.configure(text="Location", background="gray")
        self.loc_button.place(x=150, y=560, width=70, height=30)

        #Display------------
        self.text = Text(self.myParent)
        self.text.place(x=300,y=50,width =400,height=500)

    # ----- Functions -----
    #location button
    def button4Click(self, event=None):
        global ID
        self.text.delete('1.0',END)
        blockpath = os.getcwd() + "\\_BlockStorage"
        files = glob.glob(blockpath+"/*")
        file_num = 0
        ip_list = {}

        # load block to json
        for x in files:
            if not os.path.isdir(x):
                if not x[-4:] == "json":
                    if(x[-1:]) != '1':
                        shutil.copyfile(x,x+'.json')
                        file_num +=1

        # load json to dict
        json_files = glob.glob(blockpath+"/*")
        for x in json_files:
            if x[-4:] == "json":
                with open(x,'r') as f:
                    data = json.load(f)
                tx = []
                temp_dict = []
                for i in range(len(data["tx_list"])):
                    tx.append(data["tx_list"][i])
                    temp_dict.append(eval(tx[i]))
                for j in range(len(temp_dict)):
                    if 'tx_body' in temp_dict[j]["extra_data"]:
                        if temp_dict[j]["extra_data"]['tx_body']['PI_UUID'] == ID:
                            ip_list[temp_dict[j]["timestamp"]] = (temp_dict[j]["sender_ip"],temp_dict[j]["extra_data"]['tx_body']["Time"])
                            sort_ip_list = sorted(ip_list.items(),key=operator.itemgetter(0))

        string = str(sort_ip_list[0][1][0]) + " start at " + str(sort_ip_list[0][0]) +'\n'
        self.text.insert('insert',string)
        string =sort_ip_list[0][1][0] + ", "+node_info[str(sort_ip_list[0][1][0])] + '\n'
        self.text.insert('insert',string)
        for i in range(1,len(sort_ip_list)):
            if sort_ip_list[i][1][0] != sort_ip_list[i-1][1][0]:
                string2 = str(sort_ip_list[i - 1][1][0]) + " -> " + str(sort_ip_list[i][1][0]) + " at " + str(sort_ip_list[i][0]) +'\n'
                self.text.insert('insert', string2)
                string2 = sort_ip_list[i][1][0] + ", " + node_info[str(sort_ip_list[i][1][0])] + '\n'
                self.text.insert('insert',string2)
        files2 = glob.glob(blockpath + "/*")
        for y in files2:
            if not os.path.isdir(y):
                if y[-4:] == 'json':
                    os.remove(y)
    # Add Button
    def button3Click(self, event=None):
        global contents_list
        global Date
        global ID
        self.text.delete('1.0',END)

        # ID process
        if (len(self.ID_input.get()) != 0 or (len(ID) != 0) and len(self.ID_input.get()) != 0):
            self.text.insert('insert', self.ID_input.get() + '\n')
            ID = self.ID_input.get()
        else:
            if len(ID) == 0:
                self.text.insert('insert', 'Invalid Device ID \n')
            else:
                self.text.insert('insert', ID + '\n')

        # Contents Process
        if len(self.Contents_input.get()) == 0 or isNumber(self.Time_input.get()) == False or (isNumber(self.Value_input.get()) == False and isNumber(self.Value2_input.get()) == False):
            for i in range(len(contents_list)):
                self.text.insert('insert', contents_list[i])
                self.text.insert('insert', '\n')
            self.text.insert('insert', 'Invalid Input \n')
        else:
            item = {}
            item['Contents'] = self.Contents_input.get()
            if isNumber(self.Value_input.get()) == True:
                item['Upper Bound'] = self.Value_input.get()
            if isNumber(self.Value2_input.get()) == True:
                item['Lower Bound'] = self.Value2_input.get()
            item['Time'] = self.Time_input.get()
            for i in range(len(contents_list)):
                if contents_list[i]['Contents'] == item['Contents']:
                    del contents_list[i]
                    break
            contents_list.append(item)
            for i in range(len(contents_list)):
                self.text.insert('insert', contents_list[i])
                self.text.insert('insert', '\n')

        # Date Process
        try:
            if self.Date_input.get() == "0" :
                Date = 0
                self.text.insert('insert', 'Date Doesn\'t matter' )
            else:
                time.mktime(datetime.datetime.strptime(self.Date_input.get(),'%Y-%m-%d %H:%M:%S').timetuple())
                Date = self.Date_input.get()
                self.text.insert('insert', 'Goal Date :' + Date)
        except:
            if Date == 0 :
                self.text.insert('insert', 'Date Doesn\'t matter' )
            else:
                self.text.insert('insert', 'Goal Date :' + Date)
    # submit button
    def button1Click(self, event=None):
        global contents_list
        global Date
        global ID
        ip = self.IP_input.get()
        deploy_url = "http://"+ip+":5000/contract/deploy/"

        if len(ID) != 0:
            # set smart Contract info from text edit
            contract_title = "Supply Chain"
            contract_body =  '''import os
import glob
import shutil
import time
import datetime
import json
import pickle
        
class Contract:

    def __init__(self,ID,Data,Date):
        self.ID = ID
        self.Data = Data
        self.Date = Date
        with open(ID, 'wb') as k:
            pickle.dump(Data,k)

    def time2int(self,Date):
        return time.mktime(datetime.datetime.strptime(Date,'%Y-%m-%d %H:%M:%S').timetuple())

    def check_data(self,content_info,dict):
        Time_Check = 0
        Time_hold = 0
        content = content_info["Contents"]
        if 'Uppere Bound' in content_info:
            up_th_value = int(content_info["Upper Bound"])
        if 'Lower Bound' in content_info:
            lo_th_value = int(content_info["Lower Bound"])
        th_time = int(content_info["Time"]) * 60
        print ("Check",content)
        for i in range(len(dict)):
            tx_time = dict[i]['extra_data']['tx_body']['Time']
            tx_time_unix = self.time2int(tx_time)
            tx_value = int(dict[i]['extra_data']['tx_body'][content])
            print(content, i, tx_time, ":",tx_value)

            if tx_time_unix > self.time2int(self.Date):
                print("Exceeded due Date")
                string = "Exceeded due Date"
                return False,string
            if 'Lower Bound' in content_info and  'Upper Bound' in content_info:
                if (tx_value > up_th_value) or (tx_value < lo_th_value):
                    if Time_Check == 0:
                        Time_hold = tx_time_unix
                        Date_hold = dict[i]['extra_data']['tx_body']['Time']
                        Time_Check = 1
                    if (tx_time_unix - Time_hold) > th_time :
                        print(content,"exceed the limit value for ",(tx_time_unix - Time_hold),'sec From',Date_hold,'to',dict[i]['extra_data']['tx_body']['Time'] )
                        string = content + " exceed the limit value for " + str(tx_time_unix - Time_hold) + 'sec From',Date_hold,'to',dict[i]['extra_data']['tx_body']['Time']
                        return False,string
                else:
                    Time_Check = 0
            elif 'Lower Bound' in content_info:
                if (tx_value < lo_th_value):
                    if Time_Check == 0:
                        Time_hold = tx_time_unix
                        Date_hold = dict[i]['extra_data']['tx_body']['Time']
                        Time_Check = 1
                    if (tx_time_unix - Time_hold) > th_time :
                        print(content,"exceed the limit value for ",(tx_time_unix - Time_hold),'sec From',Date_hold,'to',dict[i]['extra_data']['tx_body']['Time'] )
                        string = content + " exceed the limit value for " + str(tx_time_unix - Time_hold) + 'sec From',Date_hold,'to',dict[i]['extra_data']['tx_body']['Time']
                        return False,string
                else:
                    Time_Check = 0
            elif 'Upper Bound' in content_info:
                if (tx_value > up_th_value):
                    if Time_Check == 0:
                        Time_hold = tx_time_unix
                        Date_hold = dict[i]['extra_data']['tx_body']['Time']
                        Time_Check = 1
                    if (tx_time_unix - Time_hold) > th_time :
                        print(content,"exceed the limit value for ",(tx_time_unix - Time_hold),'sec From',Date_hold,'to',dict[i]['extra_data']['tx_body']['Time'] )
                        string = content + " exceed the limit value for " + str(tx_time_unix - Time_hold) + 'sec From',Date_hold,'to',dict[i]['extra_data']['tx_body']['Time']
                        return False,string
                else:
                    Time_Check = 0
        return True,"No problem"

    def Check_contract(self):
        blockpath = os.getcwd() + "\\_BlockStorage"
        files = glob.glob(blockpath+"/*")
        file_num = 0
        dict = []

        # load block to json
        for x in files:
            if not os.path.isdir(x):
                if not x[-4:] == "json":
                    if(x[-1:]) != '1':
                        shutil.copyfile(x,x+'.json')
                        file_num +=1

        # load json to dict
        json_files = glob.glob(blockpath+"/*")
        for x in json_files:
            if x[-4:] == "json":
                with open(x,'r') as f:
                    data = json.load(f)
                tx = []
                temp_dict = []
                for i in range(len(data["tx_list"])):
                    tx.append(data["tx_list"][i])
                    temp_dict.append(eval(tx[i]))
                for j in range(len(temp_dict)):
                    if 'tx_body' in temp_dict[j]["extra_data"]:
                        if temp_dict[j]["extra_data"]['tx_body']['PI_UUID'] == self.ID:
                            dict.append(temp_dict[j])

        # delete temp json file
        files2 = glob.glob(blockpath + "/*")
        for y in files2:
            if not os.path.isdir(y):
                if y[-4:] == 'json':
                    os.remove(y)

        # check data
        for j in range(len(self.Data)):
            content_info = self.Data[j]
            if not self.check_data(content_info,dict)[0]:
                return 'Contract Destroyed',self.check_data(content_info,dict)[1]

        return "Contract Safe"

    def Check_location(self):
        blockpath = os.getcwd() + "\\_BlockStorage"
        files = glob.glob(blockpath+"/*")
        file_num = 0
        ip_list = {}

        # load block to json
        for x in files:
            if not os.path.isdir(x):
                if not x[-4:] == "json":
                    if(x[-1:]) != '1':
                        shutil.copyfile(x,x+'.json')
                        file_num +=1
        # load json to dict

        json_files = glob.glob(blockpath+"/*")
        for x in json_files:
            if x[-4:] == "json":
                with open(x,'r') as f:
                    data = json.load(f)
                tx = []
                temp_dict = []
                for i in range(len(data["tx_list"])):
                    tx.append(data["tx_list"][i])
                    temp_dict.append(eval(tx[i]))
                for j in range(len(temp_dict)):
                    if 'tx_body' in temp_dict[j]["extra_data"]:
                        if temp_dict[j]["extra_data"]['tx_body']['PI_UUID'] == self.ID:
                            ip_list[temp_dict[j]["timestamp"]] = (temp_dict[j]["sender_ip"],temp_dict[j]["extra_data"]['tx_body']["Time"])
                            sort_ip_list = sorted(ip_list.items(),key=operator.itemgetter(0))
        for i in range(1,len(sort_ip_list)):
            if sort_ip_list[i][1][0] != sort_ip_list[i-1][1][0]:
                print("ip :",sort_ip_list[i-1][1][0],"->",sort_ip_list[i][1][0],"at",sort_ip_list[i][0])
        files2 = glob.glob(blockpath + "/*")
        for y in files2:
            if not os.path.isdir(y):
                if y[-4:] == 'json':
                    os.remove(y)
        return "Last location ip"+ str(sort_ip_list[-1][1][0])
    '''
            args = []
            args.append(ID)
            args.append(contents_list)
            if Date != 0:
                args.append(Date)
            contract_args = args
            try:
                smartContract=smart_contract.generate_smartcontract(contract_title,contract_body,contract_args)
                response=request_test.deploy_smartContract(deploy_url,smartContract)
                print(str(response.text))
            except Exception as e :
                print(e)
        else:
            self.text.insert('insert','INVALID DEVICE ID!!!')
    # check button
    def button2Click(self, event=None):
        run_contract_url = "http://163.239.195.120:5000/contract/execute/"
        contract_addr= self.Address_input.get()
        contract_function="Check_contract"
        contract_args=''

        try:
            runSmartContract= run_smartcontract.generate_runSmartContract(contract_addr,contract_function,contract_args)
            response = request_test.run_smartContract(run_contract_url,runSmartContract)
            print(response.text)
        except Exception as e:
            print(e)

class Contract:

    def __init__(self,ID,Data,Date):
        self.ID = ID
        self.Data = Data
        self.Date = Date
        with open(ID, 'wb') as k:
            pickle.dump(Data,k)

    def time2int(self,Date):
        return time.mktime(datetime.datetime.strptime(Date,'%Y-%m-%d %H:%M:%S').timetuple())

    def check_data(self,content_info,dict):
        Time_Check = 0
        Time_hold = 0
        content = content_info["Contents"]
        if 'Uppere Bound' in content_info:
            up_th_value = int(content_info["Upper Bound"])
        if 'Lower Bound' in content_info:
            lo_th_value = int(content_info["Lower Bound"])
        th_time = int(content_info["Time"]) * 60
        print ("Check",content)
        for i in range(len(dict)):
            tx_time = dict[i]['extra_data']['tx_body']['Time']
            tx_time_unix = self.time2int(tx_time)
            tx_value = int(dict[i]['extra_data']['tx_body'][content])
            print(content, i, tx_time, ":",tx_value)

            if tx_time_unix > self.time2int(self.Date):
                print("Exceeded due Date")
                string = "Exceeded due Date"
                return False,string
            if 'Lower Bound' in content_info and  'Upper Bound' in content_info:
                if (tx_value > up_th_value) or (tx_value < lo_th_value):
                    if Time_Check == 0:
                        Time_hold = tx_time_unix
                        Date_hold = dict[i]['extra_data']['tx_body']['Time']
                        Time_Check = 1
                    if (tx_time_unix - Time_hold) > th_time :
                        print(content,"exceed the limit value for ",(tx_time_unix - Time_hold),'sec From',Date_hold,'to',dict[i]['extra_data']['tx_body']['Time'] )
                        string = content + " exceed the limit value for " + str(tx_time_unix - Time_hold) + 'sec From',Date_hold,'to',dict[i]['extra_data']['tx_body']['Time']
                        return False,string
                else:
                    Time_Check = 0
            elif 'Lower Bound' in content_info:
                if (tx_value < lo_th_value):
                    if Time_Check == 0:
                        Time_hold = tx_time_unix
                        Date_hold = dict[i]['extra_data']['tx_body']['Time']
                        Time_Check = 1
                    if (tx_time_unix - Time_hold) > th_time :
                        print(content,"exceed the limit value for ",(tx_time_unix - Time_hold),'sec From',Date_hold,'to',dict[i]['extra_data']['tx_body']['Time'] )
                        string = content + " exceed the limit value for " + str(tx_time_unix - Time_hold) + 'sec From',Date_hold,'to',dict[i]['extra_data']['tx_body']['Time']
                        return False,string
                else:
                    Time_Check = 0
            elif 'Upper Bound' in content_info:
                if (tx_value > up_th_value):
                    if Time_Check == 0:
                        Time_hold = tx_time_unix
                        Date_hold = dict[i]['extra_data']['tx_body']['Time']
                        Time_Check = 1
                    if (tx_time_unix - Time_hold) > th_time :
                        print(content,"exceed the limit value for ",(tx_time_unix - Time_hold),'sec From',Date_hold,'to',dict[i]['extra_data']['tx_body']['Time'] )
                        string = content + " exceed the limit value for " + str(tx_time_unix - Time_hold) + 'sec From',Date_hold,'to',dict[i]['extra_data']['tx_body']['Time']
                        return False,string
                else:
                    Time_Check = 0
        return True,"No problem"

    def Check_contract(self):
        blockpath = os.getcwd() + "\\_BlockStorage"
        files = glob.glob(blockpath+"/*")
        file_num = 0
        dict = []

        # load block to json
        for x in files:
            if not os.path.isdir(x):
                if not x[-4:] == "json":
                    if(x[-1:]) != '1':
                        shutil.copyfile(x,x+'.json')
                        file_num +=1

        # load json to dict
        json_files = glob.glob(blockpath+"/*")
        for x in json_files:
            if x[-4:] == "json":
                with open(x,'r') as f:
                    data = json.load(f)
                tx = []
                temp_dict = []
                for i in range(len(data["tx_list"])):
                    tx.append(data["tx_list"][i])
                    temp_dict.append(eval(tx[i]))
                for j in range(len(temp_dict)):
                    if 'tx_body' in temp_dict[j]["extra_data"]:
                        if temp_dict[j]["extra_data"]['tx_body']['PI_UUID'] == self.ID:
                            dict.append(temp_dict[j])

        # delete temp json file
        files2 = glob.glob(blockpath + "/*")
        for y in files2:
            if not os.path.isdir(y):
                if y[-4:] == 'json':
                    os.remove(y)

        # check data
        for j in range(len(self.Data)):
            content_info = self.Data[j]
            if not self.check_data(content_info,dict)[0]:
                return 'Contract Destroyed',self.check_data(content_info,dict)[1]

        return "Contract Safe"

    def Check_location(self):
        blockpath = os.getcwd() + "\\_BlockStorage"
        files = glob.glob(blockpath+"/*")
        file_num = 0
        ip_list = {}

        # load block to json
        for x in files:
            if not os.path.isdir(x):
                if not x[-4:] == "json":
                    if(x[-1:]) != '1':
                        shutil.copyfile(x,x+'.json')
                        file_num +=1
        # load json to dict

        json_files = glob.glob(blockpath+"/*")
        for x in json_files:
            if x[-4:] == "json":
                with open(x,'r') as f:
                    data = json.load(f)
                tx = []
                temp_dict = []
                for i in range(len(data["tx_list"])):
                    tx.append(data["tx_list"][i])
                    temp_dict.append(eval(tx[i]))
                for j in range(len(temp_dict)):
                    if 'tx_body' in temp_dict[j]["extra_data"]:
                        if temp_dict[j]["extra_data"]['tx_body']['PI_UUID'] == self.ID:
                            ip_list[temp_dict[j]["timestamp"]] = (temp_dict[j]["sender_ip"],temp_dict[j]["extra_data"]['tx_body']["Time"])
                            sort_ip_list = sorted(ip_list.items(),key=operator.itemgetter(0))
        for i in range(1,len(sort_ip_list)):
            if sort_ip_list[i][1][0] != sort_ip_list[i-1][1][0]:
                print("ip :",sort_ip_list[i-1][1][0],"->",sort_ip_list[i][1][0],"at",sort_ip_list[i][0])
        files2 = glob.glob(blockpath + "/*")
        for y in files2:
            if not os.path.isdir(y):
                if y[-4:] == 'json':
                    os.remove(y)
        return "Last location ip"+ str(sort_ip_list[-1][1][0])

def supplyChain():
    root = Tk()
    root.title('Cold Chain')
    root.geometry('750x620')
    contract_GUI(root)
    root.mainloop()

if __name__ == "__main__":
    #supplyChain()
    asd = Contract