import os , subprocess , time , sys

def delays(seconds, reason = ""):
    print("----- delays() -----")
    print("Waiting for %s seconds due to %s..." %(seconds, reason))
    seconds = int(seconds)

    while seconds > 0:
        time.sleep(1)
        seconds -= 1
        second_str = "%d seconds...\r" %seconds
        print(second_str, end='')

class sim():

    # Variables will be cleared after a RobotFramework test case executing
    ROBOT_LIBRARY_SCOPE = "GLOBAL"

    def __init__(self):
        self.sim_mapping = {}
        self.process_pid = None
		
    def init(self, sim_path, port, vbs, alias="default"):
        
        self.sim_mapping.update({alias: {}})

        self.sim_path = sim_path
        self.port = port
        self.vb_script_path = vbs

        if "/" in self.sim_path:
            self.name = self.sim_path.split("/")[-1]
        else:
            self.name = self.sim_path
        name = self.name
        self.Local_Close_All_ModRSsim_Programs()

        self.sim_mapping[alias]["config"] = vbs
        self.sim_mapping[alias]["exec"] = sim_path
        self.sim_mapping[alias]["port"] = port
        self.sim_mapping[alias]["name"] = name
		
        self.open(alias)
		
    def open(self , alias):
        print("----- Local_Open_ModRSsim_Program() -----")
        
        self.sim_path = self.sim_mapping.get(alias)["exec"]
        self.port = self.sim_mapping.get(alias)["port"]
        self.name = self.sim_mapping.get(alias)["name"]
		
        print("Connect to port : %s" %self.port)
        self.Local_Check_ModRSsim_Program_Port_State()
        if self.state:
            raise Exception("The port %s is in using" %self.port)
        else:
            cmd = 'wmic Process call create "' + self.sim_path + " modtcp:" + str(self.port) + '" | find "ProcessId"'
            cmd_result = subprocess.check_output(cmd, shell=True)
            self.process_pid = ((str(cmd_result).replace(" " ,"")).split("=")[1]).split(";")[0]
            delays(3 , "Simulator is opening")
            self.sim_mapping[alias]["pid"] = self.process_pid
            self.Local_Verify_ModRSsim_Program_State_By_PID(True , alias)


    def Local_Close_All_ModRSsim_Programs(self):
        print("----- Local_Close_All_ModRSsim_Programs() -----")
        self.Local_Get_ModRSsim_Program_State_By_Name()
        if self.state == 1:
            print("All Simulators are already closed")
            return True
        else:
            cmd = "TASKKILL /F /IM " + self.name
            subprocess.check_output(cmd, shell=True)
            delays(1 , "Simulator is closing")
            self.Local_Get_ModRSsim_Program_State_By_Name()
            if self.state == 0:
                raise Exception("All Simulators are not closed")
            else:
                print("All Simulators are closed")
                return True

    def Local_Close_ModRSsim_Program_By_PID(self , alias):
        print("----- Local_Close_ModRSsim_Program_By_PID() -----")
        self.process_pid = self.sim_mapping[alias]["pid"]
        if self.process_pid == None:
            print("No Simulator was opened")
            return
        state = self.Local_Get_ModRSsim_Program_State_By_PID(alias)
        if state:
            cmd = "wmic process " + self.process_pid + " delete"
            subprocess.check_output(cmd, shell=True)
            delays(1 , "Simulator is closing")
            self.Local_Verify_ModRSsim_Program_State_By_PID(False , alias)
        else:
            print("Simulator on PID : %s is not alive" %self.process_pid)

    def Local_Get_ModRSsim_Program_State_By_PID(self , alias):
        print("----- Local_Get_ModRSsim_Program_State_By_PID() -----")
        process_pid = self.sim_mapping[alias]["pid"]
        cmd = 'tasklist /fi "pid eq ' + process_pid + '"'
        cmd_result = subprocess.check_output(cmd, shell=True)
        if "PID" in str(cmd_result):
            print("Simulator on PID : %s is alive" %process_pid)
            return True
        else:
            print("Simulator on PID : %s is not alive" %process_pid)
            return False

    def Local_Verify_ModRSsim_Program_State_By_PID(self , expected_state , alias):
        print("----- Local_Verify_ModRSsim_Program_State_By_PID() -----")
        state = self.Local_Get_ModRSsim_Program_State_By_PID(alias)
        if expected_state:
            if state:
                print("Simulator on PID : %s is alive" %self.process_pid)
                return True
            else:
                raise Exception("Simulator on PID : %s is not alive" %self.process_pid)
        else:
            if state:
                raise Exception("Simulator on PID : %s is still alive" %self.process_pid)
            else:
                print("Simulator on PID : %s is not alive" %self.process_pid)
                return True

    def Local_Get_ModRSsim_Program_State_By_Name(self):
        print("----- Local_Get_ModRSsim_Program_State_By_Name() -----")
        self.state = os.system("TASKLIST | FINDSTR /I " + self.name)

    def Local_Check_ModRSsim_Program_Port_State(self):
        print("----- Local_Check_ModRSsim_Program_Port_State() -----")
        # Find the opened Simulator ports
        cmd_result = subprocess.check_output("hostname", shell=True)
        hostname = str(cmd_result)[2:-5]
        cmd = 'WMIC.exe process list | findstr "' + self.sim_path + ' modtcp:"'
        cmd_result = subprocess.check_output(cmd, shell=True)
        cmd_result = str(cmd_result).replace(" " ,"")
        cmd_result = cmd_result.split(self.name)

        self.state = False
        for item in cmd_result:
            if "modtcp:" in item and "findstr" not in item:
                test_port = (item.split(hostname)[0]).split("modtcp:")[1]
                if test_port == str(self.port):
                    self.state = True
                    break

    def Get_Simulator_Config_Data(self , file_path , alias):
        print("----- Get_Simulator_Config_Data() -----")
        print("Read Lines from file : " + file_path)

        if not os.path.isfile(file_path):
            raise Exception("File doesn't exists")

        with open(file_path,'r' , encoding="utf-8") as File_Test:
            file_read = File_Test.readlines()

        print(file_read)

        # Remove the empty row
        empty_index = []
        for i in range(len(file_read)):
            if ",," in file_read[i]:
                empty_index.append(i)

        empty_index.reverse()
        for item in empty_index:
            del file_read[item]

        address_list = []
        config_data_dict = {}

        # Get data type index
        if file_read[0][-1] == "\n":
            file_read[0] = file_read[0][:-1]
        data_list = file_read[0].split(",")

        address_index = -1
        data_index = -1
        expecteddata_index = -1

        for i in range(len(data_list)):
            # To avoid Case Sensitive
            current_data_type = data_list[i].lower()

            if current_data_type == "address":
                address_index = i
            elif current_data_type == "data":
                data_index = i
            elif current_data_type == "expecteddata":
                expecteddata_index = i

        # Detect the invalid data type
        if address_index == -1:
            raise Exception("No config data type : address")
        if data_index == -1:
            raise Exception("No config data type : data")
        if expecteddata_index == -1:
            raise Exception("No config data type : expecteddata")

        # To remove the title , because the next for loop doesn't need the title strings
        del file_read[0]

        simulator_data = {}
        ui_data = {}

        # Verify and Return wanted data lists
        for item in file_read:
            temp_simulator_config_data = {}

            # Remove the newline character
            if item[-1] == "\n":
                item = item[:-1]

            temp = item.split(",")

            # Verify Address range
            current_address = temp[address_index].replace(" ", "")
            if int(current_address) not in (list(range(0, 65536)) + list(range(100000,165537)) + list(range(300000,365537)) + list(range(400000,465537))):
                raise Exception("The address : %s is out of range" %current_address)

            # Verify Data range
            current_data = temp[data_index].replace(" ", "")
            if int(current_data) < -32767:
                raise Exception("The data %s on address %s is smaller than -32767" %(temp[data_index] , temp[address_index]))
            if int(current_data) > 32767:
                raise Exception("The data %s on address %s is larger than 32767" %(temp[data_index] , temp[address_index]))

            address_list.append(current_address)

            temp_simulator_config_data["address"] = current_address
            temp_simulator_config_data["data"] = current_data

            simulator_data[current_address] = temp_simulator_config_data
            ui_data[current_address] = temp[expecteddata_index]

        # Check the duplicated address
        test_address = set([x for x in address_list if address_list.count(x) > 1])
        if len(test_address) > 0:
            raise Exception("The below addresses are duplicated : ")

        self.simulator_data = simulator_data
        self.sim_mapping[alias]["simulator_data"] = simulator_data
        self.sim_mapping[alias]["ui_data"] = ui_data

        return True

    def Get_Sim_Config_Data_All(self , alias):
        return self.sim_mapping[alias]["simulator_data"]
    def Get_UI_Expected_Data_All(self , alias):
        return self.sim_mapping[alias]["ui_data"]
    def Get_Sim_Config_Data_Single(self , address , alias):
        return self.sim_mapping[alias]["simulator_data"][address]
    def Get_UI_Expected_Data_Single(self , address , alias):
        return self.sim_mapping[alias]["ui_data"][address]

    def Write_Full_Register_Address(self , alias):
        print("----- Write_Full_Register_Address() -----")
        with open(self.vb_script_path ,'w+') as f:
            simulator_data = self.sim_mapping[alias]["simulator_data"]
            for key,value in simulator_data.items():
                addresstype = value["address"][0]

                # Coil Outputs
                if addresstype == "0":
                    start_address = 0
                    vb_function_code = "0"

                # Digital Inputs
                elif addresstype == "1":
                    start_address = 100001
                    vb_function_code = "1"

                # Analog Inputs
                elif addresstype == "3":
                    start_address = 300001
                    vb_function_code = "2"

                # Holding Regs
                elif addresstype == "4":
                    start_address = 400001
                    vb_function_code = "3"

                test_address_shift = int(value["address"])-start_address
                f.write("SetRegisterValue " + vb_function_code + ", " + str(test_address_shift) + ", " + str(value["data"]) + "\n")

        print("Write Full Register Address successfully !!!")
        return True

    def Change_Register_Address_Data(self , change_data_list , alias):
        print("----- Change_Register_Address_Data() -----")

        simulator_data = self.sim_mapping.get(alias)["simulator_data"]
        ui_data = self.sim_mapping.get(alias)["ui_data"]

        for item in change_data_list:
            current_data = {k.lower(): v for k, v in item.items()}
            temp_dict = {}
            temp_sub_dict = {}

            print("###############################")
            print("Modify Address     : %s" %str(current_data["address"]))
            print("Modify Data        : %s" %str(current_data["data"]))
            print("Modify ExData      : %s" %str(current_data["expecteddata"]))
            print("###############################")

            # Verify Address range
            test_address = current_data["address"].replace(" ", "")
            if int(test_address) not in (list(range(0, 65536)) + list(range(100000,165537)) + list(range(300000,365537)) + list(range(400000,465537))):
                raise Exception("The address : %s is out of range" %test_address)

            # Verify Data range
            test_data = current_data["data"].replace(" ", "")
            if int(test_data) < -32767:
                raise Exception("The data %s on address %s is smaller than -32767" %(test_data["data"] , test_data["address"]))

            if int(test_data) > 32767:
                raise Exception("The data %s on address %s is larger than 32767" %(test_data["data"] , test_data["address"]))

            temp_sub_dict["address"] = current_data["address"]
            temp_sub_dict["data"] = current_data["data"]

            simulator_data[current_data["address"]] = temp_sub_dict
            ui_data[current_data["address"]] = current_data["expecteddata"]

        self.sim_mapping[alias]["simulator_data"] = simulator_data
        self.sim_mapping[alias]["ui_data"] = ui_data

        return True

    def Read_Config_Data_And_Write_Register(self , file_path , alias):

        self.Local_Close_ModRSsim_Program_By_PID(alias)
        self.Get_Simulator_Config_Data(file_path , alias)
        self.Write_Full_Register_Address(alias)
        self.open(alias)

    def Change_Config_Data_And_Write_Register(self, change_data , alias):

        self.Local_Close_ModRSsim_Program_By_PID(alias)
        self.Change_Register_Address_Data(change_data , alias)
        self.Write_Full_Register_Address(alias)
        self.open(alias)

if __name__ == "__main__":

    sim_script_path = "C:/Users/tkao/Documents/RobotFramework/Alber work/Automation_New_2020.02.14/BXE_Test/config_file/modbus_sim_tool_script.txt"

    sim_path_1 = "C:/Users/tkao/Documents/RobotFramework/Alber work/Automation_New_2020.02.14/BXE_Test/simulator/1/ModRSsim2_1.exe"
    sim_path_2 = "C:/Users/tkao/Documents/RobotFramework/Alber work/Automation_New_2020.02.14/BXE_Test/simulator/2/ModRSsim2_2.exe"

    sim_port_1 = 502
    sim_port_2 = 503

    config_file_1 = "C:/Users/tkao/Documents/RobotFramework/Alber work/Automation_New_2020.02.14/BXE_Test/config_file/example_1.csv"
    config_file_2 = "C:/Users/tkao/Documents/RobotFramework/Alber work/Automation_New_2020.02.14/BXE_Test/config_file/example_2.csv"

    test = sim()
    test.init(sim_path_1 , sim_port_1, sim_script_path, "SIM1")
    test.init(sim_path_2 , sim_port_2, sim_script_path, "SIM2")

    test.Local_Close_ModRSsim_Program_By_PID("SIM2")
    test.Local_Close_ModRSsim_Program_By_PID("SIM1")

    test.Read_Config_Data_And_Write_Register(config_file_1,"SIM1")
    test.Read_Config_Data_And_Write_Register(config_file_2,"SIM2")

    change_data_list = [
                         {'Address': '300001', 'Data': '32767' , "Expecteddata" : "32767 V"}
                       ]

    test.Change_Config_Data_And_Write_Register(change_data_list,"SIM1")
    print("###################################################")
    print(test.Get_UI_Expected_Data_Single('300001' , "SIM1"))
    print("###################################################")

    change_data_list = [
                         {'Address': '300001', 'Data': '3200' , "Expecteddata" : "3200 V"}
                       ]


    test.Change_Config_Data_And_Write_Register(change_data_list,"SIM2")
    print("###################################################")
    print(test.Get_UI_Expected_Data_Single('300001' , "SIM2"))
    print("###################################################")