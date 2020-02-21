*** Settings ***
Documentation       Compare the voltage of cell between BXE website and simulator
Resource            ../resources/setting.robot
Suite Setup         Run Keywords    Local Close All ModRSsim Programs    ${G_SIM1_MODBUS_ALIAS}
                    ...    AND      Local Close All ModRSsim Programs    ${G_SIM2_MODBUS_ALIAS}
                    ...    AND      Write Simulator         ${G_BATTERYCONFIG_1}            ${G_SIM1_MODBUS_ALIAS}
                    ...    AND      Verify Modbus Client    ${G_SIM1_MODBUS_ALIAS}          ${G_SIM1_MODBUS_PORT}

Suite Teardown      Run Keywords    Local Close All ModRSsim Programs    ${G_SIM1_MODBUS_ALIAS}
                    ...    AND      Local Close All ModRSsim Programs    ${G_SIM2_MODBUS_ALIAS}

*** Test Cases ***
Enter Battery on String1
    Login BXE              ${BXE_WEB_USERNAME}    ${BXE_Web_PASSWORD}    ${true}
    Enter Battery Systems
    Enter String1

Verify Address 301482
    Verify Cell Voltage     301482    ${G_HOME_BATTERYSYSTEMACCESS_STRING1_CELL_1}    ${G_SIM1_MODBUS_ALIAS}

Verify Address 301483
    Verify Cell Voltage     301483    ${G_HOME_BATTERYSYSTEMACCESS_STRING1_CELL_2}    ${G_SIM1_MODBUS_ALIAS}

Verify Address 301484
    Verify Cell Voltage     301484    ${G_HOME_BATTERYSYSTEMACCESS_STRING1_CELL_3}    ${G_SIM1_MODBUS_ALIAS}

*** Keywords ***
Verify Cell Voltage
    [Arguments]                             ${register_address}                 ${Cell Voltage Xpath}    ${Alias}
    Click Element Using JavaScript Xpath    ${Cell Voltage Xpath}
    ${ui_data}    Get UI Expected Data Single     ${register_address}                     ${Alias}
    Compare Cell                            ${ui_data}
    ${tooltip_id}                           Get Tooltip                         ${Cell Voltage Xpath}
    log                                     ${tooltip_id}
    Should Contain                          ${tooltip_id}                       Voltage: ${ui_data}.

Write Simulator
    [Arguments]                                ${Config_Data_Path}    ${Alias}
    Local Close ModRSsim Program By Alias      ${Alias}
    Read Config Data And Write VB Script       ${Config_Data_Path}    ${Alias}
    Local Open ModRSsim Program                ${Alias}

Modify Simulator
    [Arguments]                                ${Modify_Data}    ${Alias}
    Local Close ModRSsim Program By Alias      ${Alias}
    Change Config Data And Write VB Script     ${Modify_Data}    ${Alias}
    Local Open ModRSsim Program                ${Alias}

Verify Modbus Client
    [Arguments]             ${Alias}                   ${Port}
    ${verify_data}          Get Sim Config Data All    ${Alias}
    Modbus Client Verify    ${verify_data}             ${Port}