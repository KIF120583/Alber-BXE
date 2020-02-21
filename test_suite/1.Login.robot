*** Settings ***
Documentation       Login BXE and validate the username in BXE website
Resource            ../resources/setting.robot

*** Test Cases ***
Login BXE System Successfully - Single Browser
    Login BXE    ${BXE_WEB_USERNAME}    ${BXE_Web_PASSWORD}    ${true}

Login BXE System Successfully - Multiple Browsers
    Login BXE    ${BXE_WEB_USERNAME}    ${BXE_Web_PASSWORD}    ${true}
    Open BXE Url With Chrome
    Switch Browser    2
    Login BXE    ${BXE_WEB_USERNAME}    ${BXE_Web_PASSWORD}    ${true}
    Close Browser
    Switch Browser    1

Login BXE System Failed - Wrong Username
    Login BXE    TEST    ${BXE_Web_PASSWORD}    ${false}

Login BXE System Failed - Wrong Password
    Login BXE    ${BXE_WEB_USERNAME}    TEST    ${false}

Login BXE System Failed - Wrong Username and Password
    Login BXE    TEST    TEST    ${false}

Login BXE System Failed - Empty Username
    Logout BXE
    Enter Password       ${BXE_Web_PASSWORD}
    Verify Empty Login State    ${G_LOGIN_FAIL_EMPTY_USERNAME_TEXT}      User Name is required.    ${EMPTY} 

Login BXE System Failed - Empty Password
    Logout BXE
    Enter Account        ${BXE_WEB_USERNAME}
    Verify Empty Login State    ${G_LOGIN_FAIL_EMPTY_PASSWORD_TEXT}     ${EMPTY}                   Password is required.

Login BXE System Failed - Empty Username and Password
    Logout BXE
    Verify Empty Login State    ${G_LOGIN_FAIL_EMPTY_PASSWORD_TEXT}      User Name is required.    Password is required.

*** Keywords ***
Verify Empty Login State
    [Arguments]                      ${visible_text}    ${username_error}                     ${password_error}
    Click Page Button                ${G_LOGIN_BUTTON}
    Delays For Page Ready
    Wait Until Element Is Visible    ${visible_text}
    ${Error}                         Get Data           ${G_LOGIN_FAIL_EMPTY_USERNAME_TEXT}
    Should be equal                  ${Error}           ${username_error}
    ${Error}                         Get Data           ${G_LOGIN_FAIL_EMPTY_PASSWORD_TEXT}
    Should be equal                  ${Error}           ${password_error}