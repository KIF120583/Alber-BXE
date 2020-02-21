*** Settings ***
Library             SeleniumLibrary
Library             String
Library             system.py

Library       Simulator_APIs/Simulator_API.py
Library       Simulator_APIs/Config_File_API.py
Library       Modbus_Client_APIs/Modbus_Client_Socket.py

Resource    keywords.robot           
Resource    xpath.robot
Resource    ../testbeds.robot

