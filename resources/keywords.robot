*** Settings ***
Resource            setting.robot

*** Keywords ***

Open Url
    [Arguments]             ${browser}    ${url}
    Create WebDriver        ${browser}    ${BROWSER_DRIVER_PATH}
    Maximize Browser Window
    Go To                   ${url}
    Wait For Condition      return !!document.body

Open BXE Url With Chrome
    Open Url                         Chrome                       ${BXE_WEB_LOGIN_URL}
	Wait Until Element Is Visible    ${G_LOGIN_USERNAME_TAG}

Enter Text
    [Arguments]     ${TextXpath}         ${InputData}
    Input Text      ${TextXpath}         ${InputData}

Click Page Button
    [Arguments]                             ${ButtonXpath}
    Wait Until Element Is Visible           ${ButtonXpath}
    Click Element                           ${ButtonXpath}

Enter Account
    [Arguments]                      ${L_LOGIN_USERNAME}
    Wait Until Element Is Visible    ${G_LOGIN_USERNAME_INPUT_TEXT}      60
    Enter Text                       ${G_LOGIN_USERNAME_INPUT_TEXT}      ${L_LOGIN_USERNAME}

Enter Password
    [Arguments]                      ${L_LOGIN_PASSWORD}
    Wait Until Element Is Visible    ${G_LOGIN_PASSWORD_INPUT_TEXT}      60
	Enter Text                       ${G_LOGIN_PASSWORD_INPUT_TEXT}      ${L_LOGIN_PASSWORD}

Verify Login Successfully State
    Delays For Page Ready
	Wait Until Element Is Visible    ${G_HOME_BATTERYSYSTEMACCESS}      60
	${Login_User_Name}               Get Data                           ${G_HOME_LOGIN_USERNAME}
	Should be equal                  ${Login_User_Name}                 ${BXE_WEB_USERNAME}

Verify Login Failed State
    Delays For Page Ready
    Wait Until Element Is Visible    ${G_LOGIN_FAIL_TEXT}

Enter Battery Systems
    Delays For Page Ready
	Click Page Button                ${G_HOME_BATTERYSYSTEMACCESS}
    Wait Until Element Is Visible    ${G_HOME_BATTERYSYSTEMACCESS_CHECK}

Enter Advanced Users
    Delays For Page Ready
	Click Page Button                ${G_HOME_ADVANCEDACCESS}
    Wait Until Element Is Visible    ${G_HOME_ADVANCEDACCESS_CHECK}    60

Enter Site Manager
    Delays For Page Ready
	Click Element Using JavaScript Xpath    ${G_HOME_ADVANCEDACCESS_SITEMANAGER}
	Wait Until Element Is Visible           ${G_HOME_ADVANCEDACCESS_SITEMANAGER_TITLE}    60


Enter String1
    Delays For Page Ready
	Click Element Using JavaScript Xpath       ${G_HOME_BATTERYSYSTEMACCESS_STRING1}
    Wait Until Element Is Visible              ${G_HOME_BATTERYSYSTEMACCESS_STRING1_TITLE}      60

Login BXE
    [Arguments]          ${L_LOGIN_USERNAME}     ${L_LOGIN_PASSWORD}    ${L_LOGIN_STATE}
	Logout BXE
    Enter Account        ${L_LOGIN_USERNAME}
    Enter Password       ${L_LOGIN_PASSWORD}
	Click Page Button    ${G_LOGIN_BUTTON}

	Run Keyword If     ${L_LOGIN_STATE} == True
	...                Verify Login Successfully State
    ...     ELSE       Verify Login Failed State


Logout BXE
	Click Page Button                ${G_HOME_LOGOUT_BUTTON}
    Wait Until Element Is Visible    ${G_LOGIN_USERNAME_INPUT_TEXT}    60
    Wait Until Element Is Visible    ${G_LOGIN_PASSWORD_INPUT_TEXT}    60
    Delays                           3                                 Wait For Login Page Ready

Get Data
    [Arguments]     ${Xpath}
	${Data}         Get Text      ${Xpath}
    [Return]        ${Data}

Compare Cell
    [Arguments]                   ${ExpectedData}
	${ReturnData}                 Get Data                      ${G_HOME_BATTERYSYSTEMACCESS_STRING1_CELL_VOLTAGE}
    Log                           Cell Data is ${ReturnData}
    Should be equal as strings    ${ReturnData}                 ${ExpectedData}

Click Element Using JavaScript Xpath
    [Documentation]
	...  Click element using javascript while passing location using xpath
    [Arguments]                ${xpath}
    Execute JavaScript    document.evaluate('${xpath}',document.body,null,9,null).singleNodeValue.click();

Get Attribute
    [Arguments]                ${xpath}                 ${attribute}
    ${get_attribute_result}    Get Element Attribute    ${xpath}       ${attribute}
	[Return]                   ${get_attribute_result}

Get Tooltip
    [Arguments]                ${xpath}
    ${get_tooltip_result}      Get Element Attribute    ${xpath}    title
    [Return]                   ${get_tooltip_result}

Click Home Button
    Click Element Using JavaScript Xpath     ${G_HOME_BUTTON}

Delays For Page Ready
    [Arguments]          ${delaytime}=1
    Delays               ${delaytime}     Wait For Page Ready

