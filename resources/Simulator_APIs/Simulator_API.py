import os , subprocess , time
from Config_File_API import *

def delays(seconds, reason = ""):
    print("----- delays() -----")
    print("Waiting for %s seconds due to %s..." %(seconds, reason))
    seconds = int(seconds)

    while seconds > 0:
        time.sleep(1)
        seconds -= 1
        second_str = "%d seconds...\r" %seconds
        print(second_str, end='')

class Simulator_API:

    # Variables will be cleared after a RobotFramework test case executing
    ROBOT_LIBRARY_SCOPE = "GLOBAL"

    def __init__(self):
        self.sim_mapping = {}
        self.process_pid = None

    def __detect_alias(self, alias):
        print("----- Simulator_API.detect_alias() -----")
        if alias not in self.sim_mapping:
            raise Exception("The given Simulator Alias %s no presents" %alias)
        else:
            print("The given alias %s presents" %alias)
            return True

    def __print(self, print_message):
        print("--------------------------------------------------------")
        print(print_message)
        print("--------------------------------------------------------")

    def Local_Init_ModRSsim_Program(self, sim_path, port, alias="default"):
        print("----- Local_Init_ModRSsim_Program() -----\n")
        print("      Simulator Alias          : %s " %str(alias))
        print("      Simulator Path           : %s " %str(sim_path))
        print("      Simulator Port           : %s \n" %str(port))

        self.sim_mapping.update({alias: {}})

        self.sim_path = sim_path
        self.port = port

        if "/" in self.sim_path:
            self.name = self.sim_path.split("/")[-1]
        else:
            self.name = self.sim_path
        name = self.name

        self.sim_mapping[alias]["exec"] = sim_path
        self.sim_mapping[alias]["port"] = port
        self.sim_mapping[alias]["name"] = name
        self.sim_mapping[alias]["pid"] = None

        self.Local_Close_All_ModRSsim_Programs(alias)

    def Local_Open_ModRSsim_Program(self , alias):
        print("----- Local_Open_ModRSsim_Program -----")
        self.__detect_alias(alias)

        self.sim_path = self.sim_mapping.get(alias)["exec"]
        self.port = self.sim_mapping.get(alias)["port"]
        self.name = self.sim_mapping.get(alias)["name"]

        print("Connect to port : %s" %self.port)
        self.__Local_Check_ModRSsim_Program_Port_State()
        if self.state:
            raise Exception("The port %s is in using" %self.port)
        else:
            cmd = 'wmic Process call create "' + self.sim_path + " modtcp:" + str(self.port) + '" | find "ProcessId"'
            try:
                cmd_result = subprocess.check_output(cmd, shell=True)
                self.process_pid = ((str(cmd_result).replace(" " ,"")).split("=")[1]).split(";")[0]
                delays(3 , "Simulator is opening")
                self.sim_mapping[alias]["pid"] = self.process_pid
                self.Local_Verify_ModRSsim_Program_State_By_Alias(True , alias)
                self.__print("Local Simulator : %s is opened successfully !!!" %alias)

            except subprocess.CalledProcessError as err:
                # Exception handle for the wrong Simulator Path
                print(err)
                raise Exception("    Invalid Simulator Path : %s" %str(self.sim_path))

    def Local_Close_All_ModRSsim_Programs(self , alias):
        print("----- Local_Close_All_ModRSsim_Programs() -----")
        self.__detect_alias(alias)
        sim_name = self.sim_mapping[alias]["name"]

        self.__Local_Get_ModRSsim_Program_State_By_Name(alias)
        if self.state == 1:
            print("All Simulators are already closed")
            return True
        else:
            cmd = "TASKKILL /F /IM " + sim_name
            subprocess.check_output(cmd, shell=True)
            delays(1 , "Simulator is closing")
            self.__Local_Get_ModRSsim_Program_State_By_Name(alias)
            if self.state == 0:
                raise Exception("All Simulators are not closed")
            else:
                print("All Simulators are closed")
                return True

    def Local_Close_ModRSsim_Program_By_Alias(self , alias):
        print("----- Local_Close_ModRSsim_Program_By_Alias() -----")
        self.__detect_alias(alias)
        self.process_pid = self.sim_mapping[alias]["pid"]
        if self.process_pid == None:
            print("No Simulator was opened")
            return
        state = self.Local_Get_ModRSsim_Program_State_By_Alias(alias)
        if state:
            cmd = "wmic process " + self.process_pid + " delete"
            subprocess.check_output(cmd, shell=True)
            delays(1 , "Simulator is closing")
            self.Local_Verify_ModRSsim_Program_State_By_Alias(False , alias)
        else:
            pass

        self.__print("Simulator %s is closed by PID %s" %(alias , self.process_pid))

    def Local_Get_ModRSsim_Program_State_By_Alias(self , alias):
        print("----- Local_Get_ModRSsim_Program_State_By_Alias() -----")
        self.__detect_alias(alias)

        process_pid = self.sim_mapping[alias]["pid"]
        cmd = 'tasklist /fi "pid eq ' + process_pid + '"'
        cmd_result = subprocess.check_output(cmd, shell=True)
        if "PID" in str(cmd_result):
            return True
        else:
            return False

    def Local_Verify_ModRSsim_Program_State_By_Alias(self , expected_state , alias):
        print("----- Local_Verify_ModRSsim_Program_State_By_Alias() -----")
        self.__detect_alias(alias)

        state = self.Local_Get_ModRSsim_Program_State_By_Alias(alias)
        if expected_state:
            if state:
                self.__print("Simulator on PID : %s is alive" %self.process_pid)
                return True
            else:
                raise Exception("Simulator on PID : %s is not alive" %self.process_pid)
        else:
            if state:
                raise Exception("Simulator on PID : %s is still alive" %self.process_pid)
            else:
                self.__print("Simulator on PID : %s is not alive" %self.process_pid)
                return True

    def __Local_Get_ModRSsim_Program_State_By_Name(self , alias):
        print("----- __Local_Get_ModRSsim_Program_State_By_Name() -----")
        self.__detect_alias(alias)
        sim_name = self.sim_mapping[alias]["name"]
        self.state = os.system("TASKLIST | FINDSTR /I " + sim_name)

    def __Local_Check_ModRSsim_Program_Port_State(self):
        print("----- __Local_Check_ModRSsim_Program_Port_State() -----")
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

if __name__ == "__main__":

    sim_name_1 = "SIM1"
    sim_name_2 = "SIM2"

    sim_script_path = "C:/Users/tkao/Documents/RobotFramework/Alber work/Automation_New_2020.02.14/BXE_Test/config_file/modbus_sim_tool_script.txt"

    sim_path_1 = "C:/Users/tkao/Documents/RobotFramework/Alber work/Automation_New_2020.02.14/BXE_Test/simulator/1/ModRSsim2_1.exe"
    sim_path_2 = "C:/Users/tkao/Documents/RobotFramework/Alber work/Automation_New_2020.02.14/BXE_Test/simulator/2/ModRSsim2_2.exe"

    sim_port_1 = 502
    sim_port_2 = 503

    config_file_1 = "C:/Users/tkao/Documents/RobotFramework/Alber work/Automation_New_2020.02.14/BXE_Test/config_file/example_1.csv"
    config_file_2 = "C:/Users/tkao/Documents/RobotFramework/Alber work/Automation_New_2020.02.14/BXE_Test/config_file/example_2.csv"

    #################################
    # Test Simulator Open and Close #
    #################################
    test_sim = Simulator_API()
    test_sim.Local_Init_ModRSsim_Program(sim_path_1 , sim_port_1, sim_name_1)
#    test_sim.Local_Init_ModRSsim_Program(sim_path_2 , sim_port_2, sim_name_2)

    test_sim.Local_Open_ModRSsim_Program(sim_name_1)
#    test_sim.Local_Open_ModRSsim_Program(sim_name_2)

#    test_sim.Local_Close_All_ModRSsim_Programs(sim_name_1)
#    test_sim.Local_Close_All_ModRSsim_Programs(sim_name_2)

#    test_sim.Local_Open_ModRSsim_Program(sim_name_1)
#    test_sim.Local_Open_ModRSsim_Program(sim_name_2)

#    test_sim.Local_Close_ModRSsim_Program_By_Alias(sim_name_1)
#    test_sim.Local_Close_ModRSsim_Program_By_Alias(sim_name_2)


    ##########################################
    # Test Read and Write/Change Config Data #
    ##########################################
    test_config = Config_File_API()
    test_config.File_Init(sim_script_path , sim_name_1)

    test_sim.Local_Close_ModRSsim_Program_By_Alias(sim_name_1)
    test_config.Read_Config_Data_And_Write_VB_Script(config_file_1 , sim_name_1)
    test_sim.Local_Open_ModRSsim_Program(sim_name_1)

    test_sim.Local_Close_ModRSsim_Program_By_Alias(sim_name_1)
    test_config.Read_Config_Data_And_Write_VB_Script(config_file_2 , sim_name_1)
    test_sim.Local_Open_ModRSsim_Program(sim_name_1)


#    change_data_list = [
#                         {'Address': '300001', 'Data': '32767' , "Expecteddata" : "32767 V"} ,
#                         {'Address': '300002', 'Data': '32766' , "Expecteddata" : "32766 V"}
#                       ]
#
#    test_sim.Local_Close_ModRSsim_Program_By_Alias(sim_name_1)
#    test_config.Change_Config_Data_And_Write_VB_Script(change_data_list,sim_name_1)
#    test_sim.Local_Open_ModRSsim_Program(sim_name_1)
#
#    print(test_config.Get_UI_Expected_Data_Single('300001' , sim_name_1))
#    print(test_config.Get_UI_Expected_Data_Single('300002' , sim_name_1))
#
#    test_sim.Local_Close_ModRSsim_Program_By_Alias(sim_name_1)
