import os , subprocess , time

class Config_File_API:

    ROBOT_LIBRARY_SCOPE = "GLOBAL"

    def __init__(self):
        self.config_file_mapping = {}

    def __detect_alias(self, alias):
        print("----- Config_File_API.detect_alias() -----")

        if alias not in self.config_file_mapping:
            raise Exception("The given alias %s no presents" %alias)
        else:
            print("The given Config Data Alias %s presents" %alias)
            return True

    def File_Init(self , vb_script_path , alias="default"):
        print("----- File_Init() -----\n")
        print("      Config File Alias          : %s " %str(alias))
        print("      Simulator VB Script Path   : %s \n" %str(vb_script_path))

        if not os.path.isfile(vb_script_path):
            raise Exception("Simulator VB Script doesn't exists : %s" %str(vb_script_path))

        self.config_file_mapping.update({alias: {}})
        self.config_file_mapping[alias]["file_path"] = ""
        self.config_file_mapping[alias]["vb_script_path"] = vb_script_path
        self.config_file_mapping[alias]["simulator_data"] = {}
        self.config_file_mapping[alias]["ui_data"] = {}

    def __Get_Simulator_Config_Data(self , file_path , alias):
        print("----- __Get_Simulator_Config_Data() -----")
        self.__detect_alias(alias)

        if not os.path.isfile(file_path):
            raise Exception("Simulator Config File doesn't exists : %s" %str(file_path))

        print("Read Lines from file : " + file_path)

        with open(file_path,'r' , encoding="utf-8") as File_Test:
            file_read = File_Test.readlines()

        #print(file_read)

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

        #self.simulator_data = simulator_data
        self.config_file_mapping[alias]["simulator_data"] = simulator_data
        self.config_file_mapping[alias]["ui_data"] = ui_data

        return True

    def Get_Sim_Config_Data_All(self , alias):
        print("----- Get_Sim_Config_Data_All() -----")
        self.__detect_alias(alias)
        return self.config_file_mapping[alias]["simulator_data"]

    def Get_UI_Expected_Data_All(self , alias):
        print("----- Get_UI_Expected_Data_All() -----")
        self.__detect_alias(alias)
        return self.config_file_mapping[alias]["ui_data"]

    def Get_Sim_Config_Data_Single(self , address , alias):
        print("----- Get_Sim_Config_Data_Single() -----")
        self.__detect_alias(alias)
        return self.config_file_mapping[alias]["simulator_data"][address]

    def Get_UI_Expected_Data_Single(self , address , alias):
        print("----- Get_UI_Expected_Data_Single() -----")
        self.__detect_alias(alias)
        return self.config_file_mapping[alias]["ui_data"][address]

    def __Write_Full_Register_Address(self , alias):
        print("----- __Write_Full_Register_Address() -----")
        self.__detect_alias(alias)
        vb_script_path = self.config_file_mapping[alias]["vb_script_path"]
        with open(vb_script_path ,'w+') as f:
            simulator_data = self.config_file_mapping[alias]["simulator_data"]
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

    def __Change_Register_Address_Data(self , change_data_list , alias):
        print("----- __Change_Register_Address_Data() -----")
        self.__detect_alias(alias)

        simulator_data = self.config_file_mapping.get(alias)["simulator_data"]
        ui_data = self.config_file_mapping.get(alias)["ui_data"]

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

        self.config_file_mapping[alias]["simulator_data"] = simulator_data
        self.config_file_mapping[alias]["ui_data"] = ui_data

        return True

    def Read_Config_Data_And_Write_VB_Script(self , file_path , alias):
        self.__detect_alias(alias)
        self.__Get_Simulator_Config_Data(file_path , alias)
        self.__Write_Full_Register_Address(alias)

    def Change_Config_Data_And_Write_VB_Script(self , change_data_list , alias):
        self.__detect_alias(alias)
        self.__Change_Register_Address_Data(change_data_list , alias)
        self.__Write_Full_Register_Address(alias)


if __name__ == "__main__":

    alias_name_1 = "SIM1"
    alias_name_2 = "SIM2"

    sim_script_path = "C:/Users/tkao/Documents/RobotFramework/Alber work/Automation_New_2020.02.14/BXE_Test/config_file/modbus_sim_tool_script.txt"

    config_file_1 = "C:/Users/tkao/Documents/RobotFramework/Alber work/Automation_New_2020.02.14/BXE_Test/config_file/example_1.csv"
    config_file_2 = "C:/Users/tkao/Documents/RobotFramework/Alber work/Automation_New_2020.02.14/BXE_Test/config_file/example_2.csv"

    test = Config_File_API()
    test.File_Init(config_file_1 , sim_script_path , alias_name_1)
    test.File_Init(config_file_2 , sim_script_path , alias_name_2)

    test.Read_Config_Data_And_Write_VB_Script(alias_name_1)
    test.Read_Config_Data_And_Write_VB_Script(alias_name_2)

    change_data_list = [
                         {'Address': '300001', 'Data': '3200' , "Expecteddata" : "3200 V"} ,
                         {'Address': '300002', 'Data': '3300' , "Expecteddata" : "3300 V"}
                       ]

    test.Change_Config_Data_And_Write_VB_Script(change_data_list , alias_name_1)
