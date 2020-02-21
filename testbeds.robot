*** Variables ***
${BXE_WEB_USERNAME}         Administrator
${BXE_Web_PASSWORD}         SVteam123__
${BXE_SERVER_IP}            192.168.186.166
${BXE_WEB_LOGIN_URL}        http://${BXE_Server_IP}/BEEnterpriseWeb

${BROWSER_TYPE}             chrome
${BROWSER_DRIVER_PATH}      chromedriver.exe

${G_SIM_MODBUS_VBFILE}    C:/Users/tkao/Documents/RobotFramework/Alber work/Automation_New_2020.02.14/BXE_Test/config_file/modbus_sim_tool_script.txt

######################
# Simulator Settings #
######################
${G_SIM1_MODBUS_ALIAS}      Samsung_1
${G_SIM1_MODBUS_EXEFILE}    C:/Users/tkao/Documents/RobotFramework/Alber work/Automation_New_2020.02.14/BXE_Test/simulator/1/ModRSsim2_1.exe
${G_SIM1_MODBUS_PORT}       502
${G_SIM1_BATTERY_NAME}      testXXX
${G_SIM1_BATTERY_STRINGS}   4

${G_SIM2_MODBUS_ALIAS}      Samsung_2
${G_SIM2_MODBUS_EXEFILE}    C:/Users/tkao/Documents/RobotFramework/Alber work/Automation_New_2020.02.14/BXE_Test/simulator/2/ModRSsim2_2.exe
${G_SIM2_MODBUS_PORT}       503
${G_SIM2_BATTERY_NAME}      testXXX
${G_SIM2_BATTERY_STRINGS}   4

######################
# Config Settings    #
######################
${G_BATTERYCONFIG_1_ALIAS}  TestConfig1
${G_BATTERYCONFIG_1}        C:/Users/tkao/Documents/RobotFramework/Alber work/Automation_New_2020.02.14/BXE_Test/config_file/example_1.csv

${G_BATTERYCONFIG_2_ALIAS}  TestConfig2
${G_BATTERYCONFIG_2}        C:/Users/tkao/Documents/RobotFramework/Alber work/Automation_New_2020.02.14/BXE_Test/config_file/example_2.csv

${G_BATTERYCONFIG_3_ALIAS}  TestConfig3
${G_BATTERYCONFIG_3}        C:/Users/tkao/Documents/RobotFramework/Alber work/Automation_New_2020.02.14/BXE_Test/config_file/example_3.csv


