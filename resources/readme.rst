
Simulator and Modbus Client APIs
================================

.. contents::


Folder Structure
------------

::
   
     ───BXE_Sample
        │   testbeds.robot
        │
        ├───py_modbus_library
        │   │   Simulator_example.robot
        │   │
        │   ├───py_modbus_client
        │   │       Modbus_Client_Socket.py
        │   │       Modbus_Client_TK.py
        │   │
        │   └───py_modbus_simulator
        │           Config_File_API.py
        │           Simulator_API.py
        │
        ├───robot_web_resource
        │       
        │
        ├───test_suite
        │       base.robot
        │       login_case.robot
        │       modify_configuration.robot
        │       monitor_data.robot
        │
        └───utilities
            └───Modbus_RegisterData_Generator
                    Modbus_Generate_Config_Data.xlsm
	
	

Simulator 
------------

format data set
~~~~~~~~~~~~~~~

- Download `utilities/Modbus_RegisterData_Generator/Modbus_Generate_Config_Data.xlsm`

- Follow the readme sheet to generate a Simulator Config File

- In testbeds.robot , fill the file path
  

start / kill
~~~~~~~~~~~~~~~

- Before starting a Simulator , the below initial steps should be launched :

**Import the related library**::

        ** Settings ***
        Resource      ../testbeds.robot
        Library       py_modbus_simulator/Simulator_API.py


**Call the function keyword to init Simulator settings**::

    usage : 
    
        Local Init ModRSsim Program    ${sim_path}    ${sim_port}    ${sim_identifier}

    ex : 
	${sim_path}    Set Variable    C:/simulator/1/ModRSsim2_1.exe
	${sim_port}       Set Variable    502
	${sim_identifier}      Set Variable    Samsung_1
        Local Init ModRSsim Program          ${sim_path}    ${sim_port}    ${sim_identifier}
	
    => Result : The Simulator settings are initialed
		
		
**Continue the above step , start a Simulator with the below command**::

    usage : 
    
        Local Open ModRSsim Program    ${sim_identifier}
	
    => Result : The Simulator Samsung_1 is opened on port 502
	
	

**Continue the above step , kill a Simulator with the below command**::

    usage : 
    
        Local Close ModRSsim Program By Alias    ${sim_identifier}
	
    => Result : The Simulator Samsung_1 is closed on port 502
	
		
	
**Continue the above step , kill all Simulators when the program paths are same , follow the previous steps to create many Simulators**::

      Local Init ModRSsim Program    C:/simulator/1/ModRSsim2_1.exe    502    Samsung_1
      Local Init ModRSsim Program    C:/simulator/1/ModRSsim2_1.exe    503    Samsung_2
	  
      => Result : there are three Simulators opened on port 502 and 503 with the same Simulator program path , and the identifiers are Samsung_1 and Samsung_2
    
Call the below command to kill all opened Simulators::
    
      Local Close All ModRSsim Programs    Samsung_1

      => Result : Samsung_1 and Samsung_2 are closed due to their Simulator paths are same


See the test case "Open two Modbus Simulator and then verify state" in  `Simulator_example.robot <https://ghe.int.vertivco.com/RobotFrameworkTestLibrary/BXE_Sample/blob/py_modbus_library/py_modbus_library/Simulator_example.robot>`_

read / write / modify
~~~~~~~~~~~~~~~~~~~~~

- Before opening a Config File , the below initial steps should be launched

**Import the related library**::

    *** Settings ***
    Library       py_modbus_simulator/Config_File_API.py


**Call the function keyword to init Config File settings**::

    usage : 
    
        File Init    ${sim_vb_script_path}    ${config_file_identifier}
	
    ex : 
   
        ${sim_vb_script_path}      Set Variable    C:/simulator/1/sim_script.txt
        ${config_file_identifier}    Set Variable    Samsung_1
        File Init    ${sim_vb_script_path}    ${config_file_identifier}

    => Result : The Config File settings are initialed

- *Note : User should set the Simulator Script by manual first*


**Continue the above steps , read the given Config File and then write the data to VB Script of Simulator**::

    usage : 
    
        Read Config Data And Write VB Script       ${config_file_path}    ${config_file_identifier}

    ex :
    
        ${config_file_path}    Set Variable    C:/simulator/config_file/config.csv
	
        Read Config Data And Write VB Script       ${config_file_path}    ${config_file_identifier}

    => Result : C:/simulator/config_file/config.csv data will be converted and written to C:/simulator/1/sim_script.txt
	
	        

**Continue the above steps , modify test data to simulator**

Define the modify data within Robotframework as below::

    ${dict1}                Create Dictionary               address=301482             data=22000    expecteddata=22.00 V
    ${dict2}                Create Dictionary               address=301483             data=23000    expecteddata=23.00 V
    ${modify_data}          Create List                     ${dict1}                   ${dict2}

${modify_data} is created , and this variable can be used to change the current Config Data


**Call the below function keyword to modify Config Data and then write to VB Script of Simulator**::

    usage : 
    
        Change Config Data And Write VB Script     ${modify_data}    ${config_file_identifier}

    => Result : the Modify data will be written to C:/simulator/1/sim_script.txt


**Continue the above steps ,  , get the expected UI data with the below function keyword**::

    usage : 
    
        Get UI Expected Data Single    ${register_address}    ${sim_identifier}
	
    ex : 
   
        ${ui_data}    Get UI Expected Data Single    301482    Samsung_1
	
    => Result : ${ui_data} will be 22.00 V
	
        
-----------------------

**Note**:

- Be sure that Read and Write Config Data should be started before modifying

- After Read/Write/Modify Config Data , the Simulator should be restarted to renew the data



See the test case "Open a Modbus Simulator then Read/Write/Modify Simulator Data" in  `Simulator_example.robot <https://ghe.int.vertivco.com/RobotFrameworkTestLibrary/BXE_Sample/blob/py_modbus_library/py_modbus_library/Simulator_example.robot>`_


Modbus Client 
-------------

fetch and compare data
~~~~~~~~~~~~~~~~~~~~~~

Import the related library::

    *** Settings ***
    Library       py_modbus_client/Modbus_Client_Socket.py


**Get the current Config Simulator Data with the below function keyword**::

    ${verify_data}          Get Sim Config Data All    ${config_file_identifier}

    => Result : the Simulator Data will be stored to ${verify_data}
   
**Call the below function keyword to compare data via modbus client**::

    Modbus Client Verify    ${verify_data}    ${sim_port}

    => Result : Modbus Client session will be created and fetch the address of ${verify_data} then compare
   
See the test case "Open a Modbus Simulator then Read/Write/Modify Simulator Data" in  `Simulator_example.robot <https://ghe.int.vertivco.com/RobotFrameworkTestLibrary/BXE_Sample/blob/py_modbus_library/py_modbus_library/Simulator_example.robot>`_


    

