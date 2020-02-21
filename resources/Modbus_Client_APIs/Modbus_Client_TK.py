import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_tcp
		
class Modbus_Client_TK:

    ROBOT_LIBRARY_SCOPE = "GLOBAL"

    def __init__(self):

        self.modbus_server_ip = "127.0.0.1"

    def Modbus_Client_Open(self , port):
        print("----- Modbus_Client_Open() -----")
        print("Connect to Modbus TCP IP   : %s" %(str(self.modbus_server_ip)))
        print("Connect to Modbus TCP Port : %s" %(str(port)))

        # SOCK_STREAM : TCP/IP
        self.socketClient = modbus_tcp.TcpMaster(host=str(self.modbus_server_ip),port=int(port))
        self.socketClient.set_timeout(5.0)

    def Modbus_Client_Get_Address(self , addresstype , address):
        print("----- Modbus_Client_Get_Address() -----")
        address = int(address)
        if addresstype == "0":
            query_cmd = cst.READ_COILS
            query_address = address - 0
        elif addresstype == "1":
            query_cmd = cst.READ_DISCRETE_INPUTS
            query_address = address - 100001
        elif addresstype == "3":
            query_cmd = cst.READ_INPUT_REGISTERS
            query_address = address - 300001
        elif addresstype == "4":
            query_cmd = cst.READ_HOLDING_REGISTERS
            query_address = address - 400001

        return_value = str(self.socketClient.execute(1, query_cmd, query_address,1))[1:-2]
        if int(return_value) > 32767:
            return_value = str(int(return_value) - 65536)

        return int(return_value)

    def Modbus_Client_Get_Coil_Outputs(self , address):
        print("----- Modbus_Client_Get_Coil_Outputs() -----")
        return self.Modbus_Client_Get_Address("0" , address)

    def Modbus_Client_Get_Digital_Inputs(self , address):
        print("----- Modbus_Client_Get_Digital_Inputs() -----")
        return self.Modbus_Client_Get_Address("1" , address)

    def Modbus_Client_Get_Analog_Inputs(self , address):
        print("----- Modbus_Client_Get_Analog_Inputs() -----")
        return self.Modbus_Client_Get_Address("3" , address)

    def Modbus_Client_Get_Holding_Regs(self , address):
        print("----- Modbus_Client_Get_Holding_Regs() -----")
        return self.Modbus_Client_Get_Address("4" , address)


    def Modbus_Client_Verify(self , config_data , port):
        print("----- Modbus_Client_Verify() -----")
        self.Modbus_Client_Open(int(port))
        return_flag = True
        #print(config_data)
        for key,value in config_data.items():
            addresstype = value["address"].zfill(6)[0]
            return_data = self.Modbus_Client_Get_Address(addresstype , value["address"])
            if return_data != int(value["data"]):
                print("Orz -> Compare failed on address : %s , Return Data : %s , Expected Data : %s" %(value["address"] , str(return_data) , value["data"]))
                return_flag = False
            else:
                print("Compare success on address : %s , Return Data : %s , Expected Data : %s" %(value["address"] , str(return_data) , value["data"]))

        self.Modbus_Client_Close()

        if return_flag:
            print("Verify all addresses are pass")
        else:
            raise Exception("Verify all addresses are failed")

    def Modbus_Client_Close(self):
        print("----- Modbus_Client_Close() -----")
        self.socketClient._do_close()
        self.socketClient = None

if __name__ == "__main__":

    # Prepare a vb script for Simulator as below :
    #   SetRegisterValue 0, 4, 1
    #   SetRegisterValue 1, 3, 1
    #   SetRegisterValue 2, 1481, 22000
    #   SetRegisterValue 3, 0, 24000

    test = Modbus_Client_TK(502)

    config_data = {
                     "301482" : {"address" : "301482" , "data" : "22000"}
                  }

    test.Modbus_Client_Verify(config_data)

    test.Modbus_Client_Open()

    test = test.Modbus_Client_Get_Analog_Inputs(301482)
    print(test)
	#
    #test = test.Modbus_Client_Get_Holding_Regs(400001)
    #print(test)