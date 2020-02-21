from socket import *
import time 

def delays(seconds, reason = ""):
    print("----- delays() -----")
    print("Waiting for %s seconds due to %s..." %(seconds, reason))
    seconds = int(seconds)

    while seconds > 0:
        time.sleep(1)
        seconds -= 1
        second_str = "%d seconds...\r" %seconds
        print(second_str, end='')
		
class Modbus_Client_Socket:

    ROBOT_LIBRARY_SCOPE = "GLOBAL"

    def __init__(self):

        self.modbus_server_ip = "127.0.0.1"

        # Coil Outputs , Digital Inputs , Analog Inputs , Holding Regs
        self.addresstype = {
                              "0" : {"start_address" : 0      , "socket_cmd" : "0000000000080101" , "end_cmd" :  "00010E84"} ,
                              "1" : {"start_address" : 100001 , "socket_cmd" : "0000000000080102" , "end_cmd" :  "00010E84"} ,
                              "3" : {"start_address" : 300001 , "socket_cmd" : "0000000000060104" , "end_cmd" :  "0001"} ,
                              "4" : {"start_address" : 400001 , "socket_cmd" : "0000000000060103" , "end_cmd" :  "0001"}
                           }

    def Modbus_Client_Open(self , port):
        print("----- Modbus_Client_Open() -----")
        print("Connect to Modbus TCP IP   : %s" %(str(self.modbus_server_ip)))
        print("Connect to Modbus TCP Port : %s" %(str(port)))

        # SOCK_STREAM : TCP/IP
        self.socketClient = socket(AF_INET, SOCK_STREAM)
        self.socketClient.bind(("", 0))
        test = self.socketClient.connect((self.modbus_server_ip, int(port)))
        delays(1)

    def Modbus_Client_Get_Address(self , addresstype , address):
        print("----- Modbus_Client_Get_Address() -----")
        if addresstype not in ["0" , "1" , "3" , "4"]:
            raise Exception("The address type : %s is not supported" %addresstype)
		
        test_address_shift = int(address) - self.addresstype[addresstype]["start_address"]
        test_address_shift_hex = hex(test_address_shift)[2:].zfill(4)
        cmdBuf = bytes.fromhex(self.addresstype[addresstype]["socket_cmd"] + test_address_shift_hex + self.addresstype[addresstype]["end_cmd"])
		
        self.socketClient.send(cmdBuf)
        recvData, recvAddr = self.socketClient.recvfrom(1024)
        
        if addresstype in ["0" , "1"]:
            return recvData[9]
        else:
            return_value = recvData[9]*256+recvData[10]
            if int(return_value) > 32767:
                return_value = int(return_value) - 65536

            return return_value

    def Modbus_Client_Get_Coil_Outputs(self , address):
        print("----- Modbus_Client_Get_Coil_Outputs() -----")
        return self.Modbus_Client_Get_Address("0" , str(address))

    def Modbus_Client_Get_Digital_Inputs(self , address):
        print("----- Modbus_Client_Get_Digital_Inputs() -----")
        return self.Modbus_Client_Get_Address("1" , str(address))

    def Modbus_Client_Get_Analog_Inputs(self , address):
        print("----- Modbus_Client_Get_Analog_Inputs() -----")
        return self.Modbus_Client_Get_Address("3" , str(address))

    def Modbus_Client_Get_Holding_Regs(self , address):
        print("----- Modbus_Client_Get_Holding_Regs() -----")
        return self.Modbus_Client_Get_Address("4" , str(address))

    def Modbus_Client_Verify(self , config_data , port):
        print("----- Modbus_Client_Verify() -----")
        self.Modbus_Client_Open(int(port))
        return_flag = True

        for key,value in config_data.items():
            addresstype = value["address"].zfill(6)[0]
            return_data = self.Modbus_Client_Get_Address(addresstype , value["address"])
            if return_data != int(value["data"]):
                print("Orz -> Compare failed on address : %s , Return Data : %s , Expected Data : %s" %(value["address"] , str(return_data) , value["data"]))
                return_flag = False
            else:
                print("Compare success on address : %s , Return Data : %s , Expected Data : %s" %(value["address"] , str(return_data) , value["data"]))

        self.Modbus_Client_Close(port)

        if return_flag:
            print("Verify all addresses are pass")
        else:
            raise Exception("Verify all addresses are failed")

    def Modbus_Client_Close(self , port):
        print("----- Modbus_Client_Close() -----")
        print("Disconnect to Modbus TCP IP   : %s" %(str(self.modbus_server_ip)))
        print("Disconnect to Modbus TCP Port : %s" %(str(port)))
        return self.socketClient.close()


if __name__ == "__main__":

    # Prepare a vb script for Simulator as below :
    #   SetRegisterValue 0, 4, 1
    #   SetRegisterValue 1, 3, 1
    #   SetRegisterValue 2, 1481, 22000
    #   SetRegisterValue 3, 0, 24000

    test = Modbus_Client_Socket()

    config_data = {
                     "301482" : {"address" : "300001" , "data" : "22000"} ,
                     "100004" : {"address" : "100004" , "data" : "1"},
                  }

    #test.Modbus_Client_Verify(config_data , 503)

    test.Modbus_Client_Open(503)

    test = test.Modbus_Client_Get_Analog_Inputs(300001)
    print(test)


