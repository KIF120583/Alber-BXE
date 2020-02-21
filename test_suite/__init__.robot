*** Settings ***
Documentation       Initial Setup
Resource            ../resources/setting.robot
Resource            ../testbeds.robot        
Suite Setup        Run Keywords    Open BXE Url With Chrome
                   ...    AND      Local Init ModRSsim Program          ${G_SIM1_MODBUS_EXEFILE}    ${G_SIM1_MODBUS_PORT}    ${G_SIM1_MODBUS_ALIAS}
                   ...    AND      Local Init ModRSsim Program          ${G_SIM2_MODBUS_EXEFILE}    ${G_SIM2_MODBUS_PORT}    ${G_SIM2_MODBUS_ALIAS}
                   ...    AND      File Init                            ${G_SIM_MODBUS_VBFILE}      ${G_SIM1_MODBUS_ALIAS}
                   ...    AND      File_Init                            ${G_SIM_MODBUS_VBFILE}      ${G_SIM2_MODBUS_ALIAS}
				   
Suite Teardown     Run Keywords    Close All Browsers
                   ...    AND      Local Close All ModRSsim Programs    ${G_SIM1_MODBUS_ALIAS}
                   ...    AND      Local Close All ModRSsim Programs    ${G_SIM2_MODBUS_ALIAS}
				   

	