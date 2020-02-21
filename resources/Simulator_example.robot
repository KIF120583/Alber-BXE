*** Variables ***
#${G_SIM_MODBUS_VBFILE}    C:/Users/tkao/Documents/RobotFramework/Alber work/Automation_New_2020.02.14/BXE_Test/config_file/modbus_sim_tool_script.txt
#
#${G_SIM1_MODBUS_ALIAS}      Samsung_1
#${G_SIM1_MODBUS_EXEFILE}    C:/Users/tkao/Documents/RobotFramework/Alber work/Automation_New_2020.02.14/BXE_Test/simulator/1/ModRSsim2_1.exe
#${G_SIM1_MODBUS_PORT}       502
#
#${G_SIM2_MODBUS_ALIAS}      Samsung_2
#${G_SIM2_MODBUS_EXEFILE}    C:/Users/tkao/Documents/RobotFramework/Alber work/Automation_New_2020.02.14/BXE_Test/simulator/2/ModRSsim2_2.exe
#${G_SIM2_MODBUS_PORT}       503
#
#${G_BATTERYCONFIG_1}        C:/Users/tkao/Documents/RobotFramework/Alber work/Automation_New_2020.02.14/BXE_Test/config_file/example_1.csv

*** Settings ***
#Resource      ../testbeds.robot
#Library       py_modbus_simulator/Simulator_API.py
#Library       py_modbus_simulator/Config_File_API.py

Library       Simulator_APIs/Simulator_API.py
Library       Simulator_APIs/Config_File_API.py

Library       py_modbus_client/Modbus_Client_Socket.py
#Library       py_modbus_client/Modbus_Client_TK.py

#Suite Setup        Run Keywords    Local Init ModRSsim Program          ${G_SIM1_MODBUS_EXEFILE}    ${G_SIM1_MODBUS_PORT}    ${G_SIM1_MODBUS_ALIAS}
#                   ...    AND      Local Init ModRSsim Program          ${G_SIM2_MODBUS_EXEFILE}    ${G_SIM2_MODBUS_PORT}    ${G_SIM2_MODBUS_ALIAS}
#                   ...    AND      File Init                            ${G_SIM_MODBUS_VBFILE}      ${G_SIM1_MODBUS_ALIAS}
#                   ...    AND      File_Init                            ${G_SIM_MODBUS_VBFILE}      ${G_SIM2_MODBUS_ALIAS}
#Suite TearDown     Run Keywords    Local Close All ModRSsim Programs    ${G_SIM1_MODBUS_ALIAS}
#                   ...    AND      Local Close All ModRSsim Programs    ${G_SIM2_MODBUS_ALIAS}
#
#Test Setup         Run Keywords    Local Close All ModRSsim Programs    ${G_SIM1_MODBUS_ALIAS}
#                   ...    AND      Local Close All ModRSsim Programs    ${G_SIM2_MODBUS_ALIAS}

*** Test cases ***
######################
# Positive Test      #
######################
Open two Modbus Simulator and then verify state
    [Documentation]    Expected result : Pass
	${G_SIM1_MODBUS_EXEFILE}    Set Variable    C:/Users/tkao/Documents/RobotFramework/Alber work/Automation_New_2020.02.14/BXE_Test/simulator/1/ModRSsim2_1.exe
	${G_SIM1_MODBUS_PORT}       Set Variable    502
	${G_SIM1_MODBUS_ALIAS}      Set Variable    Samsung_1
	
	Local Init ModRSsim Program          ${G_SIM1_MODBUS_EXEFILE}    ${G_SIM1_MODBUS_PORT}    ${G_SIM1_MODBUS_ALIAS}
#	Local Init ModRSsim Program          ${G_SIM2_MODBUS_EXEFILE}    ${G_SIM2_MODBUS_PORT}    ${G_SIM2_MODBUS_ALIAS}
    Local Open ModRSsim Program              ${G_SIM1_MODBUS_ALIAS}
#    Local Open ModRSsim Program              ${G_SIM2_MODBUS_ALIAS}
    Local Close ModRSsim Program By Alias    ${G_SIM1_MODBUS_ALIAS}
#    Local Close ModRSsim Program By Alias    ${G_SIM2_MODBUS_ALIAS}
    Local Open ModRSsim Program              ${G_SIM1_MODBUS_ALIAS}

    Local Verify ModRSsim Program State By Alias    ${true}     ${G_SIM1_MODBUS_ALIAS}
#    Local Verify ModRSsim Program State By Alias    ${false}    ${G_SIM2_MODBUS_ALIAS}

#Open a Modbus Simulator then Read/Write/Modify Simulator Data
#    [Documentation]    Expected result : Pass
#    Write Simulator         ${G_BATTERYCONFIG_1}            ${G_SIM1_MODBUS_ALIAS}
#    ${ui_data}              Get UI Expected Data Single     300001                    ${G_SIM1_MODBUS_ALIAS}
#    log to console          ${ui_data}
#    Verify Modbus Client    ${G_SIM1_MODBUS_ALIAS}          ${G_SIM1_MODBUS_PORT}
#
#    ${dict1}                Create Dictionary               address=300001             data=21000    expecteddata=21.00 V
#    ${modify_data}          Create List                     ${dict1}
#    Modify Simulator        ${modify_data}                  ${G_SIM1_MODBUS_ALIAS}
#    ${ui_data}              Get UI Expected Data Single     300001                    ${G_SIM1_MODBUS_ALIAS}
#    log to console          ${ui_data}
#    Should be equal         ${ui_data}                      21.00 V
#    Verify Modbus Client    ${G_SIM1_MODBUS_ALIAS}          ${G_SIM1_MODBUS_PORT}
#
#######################
## Negative Test      #
#######################
#Open the same Simulator twice
#    [Documentation]    Expected result : Fail
#    Local Open ModRSsim Program     ${G_SIM1_MODBUS_ALIAS}
#    Local Open ModRSsim Program     ${G_SIM1_MODBUS_ALIAS}
#
#Use the invalid Alias on Simulator
#    [Documentation]    Expected result : Fail
#    Local Open ModRSsim Program     testtest
#
#Use the invalid Config File Path
#    [Documentation]    Expected result : Fail
#    Local Open ModRSsim Program     ${G_SIM1_MODBUS_ALIAS}
#    Write Simulator                 d:/test.csv             ${G_SIM1_MODBUS_ALIAS}
#
#*** Keywords ***
#Write Simulator
#    [Arguments]                                ${Config_Data_Path}    ${Alias}
#    Local Close ModRSsim Program By Alias      ${Alias}
#    Read Config Data And Write VB Script       ${Config_Data_Path}    ${Alias}
#    Local Open ModRSsim Program                ${Alias}
#
#Modify Simulator
#    [Arguments]                                ${Modify_Data}    ${Alias}
#    Local Close ModRSsim Program By Alias      ${Alias}
#    Change Config Data And Write VB Script     ${Modify_Data}    ${Alias}
#    Local Open ModRSsim Program                ${Alias}
#
#Verify Modbus Client
#    [Arguments]             ${Alias}                   ${Port}
#    ${verify_data}          Get Sim Config Data All    ${Alias}
#    Modbus Client Verify    ${verify_data}             ${Port}
#
#