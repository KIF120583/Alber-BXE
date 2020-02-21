import paramiko
from threading import Thread
from System_APIs import *

# Functions :
#  SSH_Connect()
#  SSH_Disconnect()
#  SSH_Write()
#  SSH_Open_ModRSsim_Program()
#  SSH_Close_All_ModRSsim_Programs()
#  SSH_Close_ModRSsim_Program_By_PID()
#  SSH_Get_ModRSsim_Program_State_By_PID()
#  SSH_Get_ModRSsim_Program_State_By_Name()
#  SSH_Check_ModRSsim_Program_Port_State()
#  SSH_Write_Full_Register_Address()

class ssh_data:
    pass

class SSHConnection():

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def __init__(self , ip , port , name , password , timeout):

        self.ip = ip
        self.port = port
        self.name = name
        self.password = password
        self.timeout = timeout

    def open(self):
        try:
            self.client.connect(self.ip, port=self.port, username=self.name, password=self.password,timeout=self.timeout)
        except Exception as err:
            print("Exception in SSHConnection.open()")
            exception_handle(err)
            return False

    def send(self,SSH_Command,send_timeout):
        try:
            (stdin, stdout, stderr) = self.client.exec_command(SSH_Command, timeout=send_timeout)
            Command_return = stdout.readlines()
            return Command_return
        except Exception as err:
            print("Exception in SSHConnection.send()")
            exception_handle(err)
            return False

    def close(self):
        try:
            return self.client.close()
        except Exception as err:
            print("Exception in SSHConnection.close()")
            exception_handle(err)
            return False

def SSH_Connect(ip , port , name , password , timeout=30):
    try:
        print("----- SSH_Connect() -----")
        print("Connect to %s" %ip)
        ssh_data.con = SSHConnection(ip , port , name , password , timeout)
        ssh_data.con.open()
        return True
    except Exception as err:
        print("Exception in SSH_Connect()")
        exception_handle(err)
        return False

def SSH_Disconnect():
    try:
        print("----- SSH_Disconnect() -----")
        ssh_data.con.close()
        return True
    except Exception as err:
        print("Exception in SSH_Connect()")
        exception_handle(err)
        return False

# return type : List
def SSH_Write(command,ssh_write_timeout=10):
    try:
        print("----- SSH_Write() -----")
        print("SSH_Write Command : "+command)
        SSH_Result = ssh_data.con.send(command,ssh_write_timeout)
        #print("SSH Response : %s " %SSH_Result)
        return SSH_Result

    except Exception as err:
        print("Exception in SSH_Write()")
        exception_handle(err)
        return False

def SSH_Open_ModRSsim_Program(ssh_modbus_sim_tool_path , ssh_modbus_sim_tool_port):
    try:
        print("----- SSH_Open_ModRSsim_Program() -----")
        #modbus_sim_tool_name = ssh_modbus_sim_tool_path.split("/")[-1]
        if "/" in modbus_sim_tool_path:
            modbus_sim_tool_name = modbus_sim_tool_path.split("/")[-1]
        else:
            modbus_sim_tool_name = modbus_sim_tool_path

        response_before = SSH_Write("TASKLIST | findstr /i " + modbus_sim_tool_name)
        # Example for response_before:
        #['ModRSsim2.exe                 4600 Services                   0     12,828 K\r\n']

        pid_before = []
        for item in response_before:
            test = ((item.replace(" ","")).split(modbus_sim_tool_name)[1]).split("Services")[0]
            pid_before.append(test)
        # Example for pid_before:
        #['4600']

        modsim_open_thread = Thread(target=SSH_Write, args=(ssh_modbus_sim_tool_path + " modtcp:" + str(ssh_modbus_sim_tool_port) + " &" , 120) ,name="SSH_ModRSsim_Program_Open")
        modsim_open_thread.setDaemon(True)
        modsim_open_thread.start()

        delays(5 , "Wait for Simulator ready")
        response_after = SSH_Write("TASKLIST | findstr /i " + modbus_sim_tool_name)

        pid_after = []
        for item in response_after:
            test = ((item.replace(" ","")).split(modbus_sim_tool_name)[1]).split("Services")[0]
            pid_after.append(test)

        # Find the new pid and return
        for item in pid_after:
            if item not in pid_before:
                return item

    except Exception as err:
        print("Exception in SSH_Open_ModRSsim_Program()")
        exception_handle(err)
        return False

def SSH_Close_All_ModRSsim_Programs(ssh_modbus_sim_tool_path):
    try:
        print("----- SSH_Close_All_ModRSsim_Program() -----")
        #modbus_sim_tool_name = ssh_modbus_sim_tool_path.split("/")[-1]
        if "/" in modbus_sim_tool_path:
            modbus_sim_tool_name = modbus_sim_tool_path.split("/")[-1]
        else:
            modbus_sim_tool_name = modbus_sim_tool_path
        SSH_Write("TASKKILL /F /IM " + modbus_sim_tool_name)

        # Check All SSH ModRSsim programs are killed
        ssh_state = SSH_Get_ModRSsim_Program_State_By_Name(modbus_sim_tool_name)
        if ssh_state:
            print("%s is not closed" %modbus_sim_tool_name)
            return False
        else:
            print("%s is closed" %modbus_sim_tool_name)
            return True

    except Exception as err:
        print("Exception in SSH_Close_All_ModRSsim_Programs()")
        exception_handle(err)
        return False

def SSH_Close_ModRSsim_Program_By_PID(process_pid):
    try:
        print("----- SSH_Close_ModRSsim_Program_By_PID() -----")
        SSH_Write('TASKKILL /fi "pid eq ' + process_pid + '"')
    except Exception as err:
        print("Exception in SSH_Close_ModRSsim_Program_By_PID()")
        exception_handle(err)
        return False

def SSH_Get_ModRSsim_Program_State_By_PID(process_pid):
    try:
        print("----- SSH_Get_ModRSsim_Program_State_By_PID() -----")
        response = SSH_Write('TASKLIST /fi "pid eq ' + process_pid + '"')
        if "No tasks are running" in response[0]:
            print("The program on PID : %s is not running" %process_pid)
            return False
        else:
            print("The program on PID : %s is running" %process_pid)
            return True
    except Exception as err:
        print("Exception in SSH_Get_ModRSsim_Program_State_By_PID()")
        exception_handle(err)
        return False

def SSH_Get_ModRSsim_Program_State_By_Name(ssh_modbus_sim_tool_path):
    try:
        print("----- SSH_Get_ModRSsim_Program_State_By_Name() -----")
        #modbus_sim_tool_name = ssh_modbus_sim_tool_path.split("/")[-1]
        if "/" in modbus_sim_tool_path:
            modbus_sim_tool_name = modbus_sim_tool_path.split("/")[-1]
        else:
            modbus_sim_tool_name = modbus_sim_tool_path
        response = SSH_Write("TASKLIST | findstr /i " + modbus_sim_tool_name)
        if len(response) > 0 :
            print("The program %s is running" %modbus_sim_tool_name)
            return True
        else:
            print("The program %s is not running" %modbus_sim_tool_name)
            return False
    except Exception as err:
        print("Exception in SSH_Get_ModRSsim_Program_State_By_Name()")
        exception_handle(err)
        return False

def SSH_Check_ModRSsim_Program_Port_State(modbus_sim_tool_path , modbus_sim_tool_port):
    try:
        print("----- SSH_Check_ModRSsim_Program_Port_State() -----")
        if "/" in modbus_sim_tool_path:
            modbus_sim_tool_name = modbus_sim_tool_path.split("/")[-1]
        else:
            modbus_sim_tool_name = modbus_sim_tool_path
        # Find the opened Simulator ports
        cmd_result = SSH_Write('/cygdrive/c/windows/system32/wbem/WMIC.exe process list | findstr "' + modbus_sim_tool_path + ' modtcp:"')
        #print(cmd_result)

        # Find the opened Simulator ports
        find_port_flag = False
        for item in cmd_result:
            if modbus_sim_tool_name + " modtcp:" in item and "findstr" not in item:
                test_port = ((item.replace(" ","")).split("modtcp:")[1]).split("DESKTOP")[0]
                if test_port == str(modbus_sim_tool_port):
                    find_port_flag = True
                    break

        return find_port_flag
    except Exception as err:
        print("Exception in SSH_Check_ModRSsim_Program_Port_State()")
        exception_handle(err)
        return False

def SSH_Write_Full_Register_Address(ssh_modbus_sim_tool_script_full_path , config_data):
    try:
        print("----- SSH_Write_Full_Register_Address() -----")
        config_string = ""
        for item in config_data:

            # Coil Outputs
            if item["addresstype"] == "0":
                start_address = 0

            # Digital Inputs
            elif item["addresstype"] == "1":
                start_address = 10001

            # Analog Inputs
            elif item["addresstype"] == "2":
                start_address = 30001

            # Holding Regs
            elif item["addresstype"] == "3":
                start_address = 40001

            test_address_shift = int(item["address"])-start_address
            config_string = config_string + "SetRegisterValue " + item["addresstype"] + ", " + str(test_address_shift) + ", " + str(item["data"]) + "\n"

        SSH_Write("echo '" + config_string + "' > " + ssh_modbus_sim_tool_script_full_path)

        print("SSH Write Full Register Address successfully !!!")
        return True

    except Exception as err:
        print("Exception in SSH_Write_Full_Register_Address()")
        exception_handle(err)
        return False

if __name__ == "__main__":

    # For test
    from Local_Sim_APIs import *
    from Modbus_Client import *
    from File_APIs import *

    ssh_server_ip = "192.168.186.169"
    ssh_server_name = "tkao"
    ssh_server_pass = "SVteam123__"
    ssh_server_port = 22
    ssh_modbus_sim_tool_path = "/home/tkao/Desktop/Samsung/ModRSsim2.exe"
    ssh_modbus_sim_tool_script_full_path = "/home/tkao/Desktop/Samsung/modbus_sim_tool_script.txt"
    modbus_sim_tool_path = "C:/Users/tkao/Desktop/Taylor/Project/Alber/Samsung/ModRSsim2.exe"

    SSH_Connect(ssh_server_ip , ssh_server_port , ssh_server_name , ssh_server_pass)

    process_pid_1 = SSH_Open_ModRSsim_Program(ssh_modbus_sim_tool_path , 512)
    test = SSH_Check_ModRSsim_Program_Port_State(modbus_sim_tool_path,512)
    print(test)

    ssh_state = SSH_Close_All_ModRSsim_Programs(ssh_modbus_sim_tool_path)
    print(ssh_state)

#    process_pid_2 = SSH_Open_ModRSsim_Program(ssh_modbus_sim_tool_path , 513)
#    process_pid_3 = SSH_Open_ModRSsim_Program(ssh_modbus_sim_tool_path , 514)
#    process_pid_4 = SSH_Open_ModRSsim_Program(ssh_modbus_sim_tool_path , 515)
#
#    #test = SSH_Get_ModRSsim_Program_State_By_Name(ssh_modbus_sim_tool_path)
#    #print(test)
#
#    test = SSH_Get_ModRSsim_Program_State_By_PID(process_pid_2)
#    print(test)
#
#    SSH_Close_ModRSsim_Program_By_PID(process_pid_2)
#
#    test = SSH_Get_ModRSsim_Program_State_By_PID(process_pid_2)
#    print(test)

#    file_read = Read_Config_Data("config_data.csv")
#    _ , config_data , _ = Get_Simulator_Config_Data(file_read)
#    SSH_Write_Full_Register_Address(ssh_modbus_sim_tool_script_full_path , config_data)
#
#    SSH_Open_ModRSsim_Program(ssh_modbus_sim_tool_path , 511)
#    Verify_Register_Data_Via_Socket(config_data , ssh_server_ip , 511)
#
#    ################################
#    # Change Single Address sample #
#    ################################
#    config_data = Modify_Single_Register_Address_Data(config_data , 31482 , 12000)
#    SSH_Close_All_ModRSsim_Programs(ssh_modbus_sim_tool_path)
#    SSH_Write_Full_Register_Address(ssh_modbus_sim_tool_script_full_path , config_data)
#    SSH_Open_ModRSsim_Program(ssh_modbus_sim_tool_path , 512)
#    Verify_Register_Data_Via_Socket(config_data , ssh_server_ip , 512)

    SSH_Disconnect()
