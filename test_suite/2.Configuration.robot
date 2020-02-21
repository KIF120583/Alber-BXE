*** Settings ***
Documentation       Modify the location information for Battery in BXE website
Resource            ../resources/setting.robot

*** Test Cases ***
Enter Site Manager Page
    Login BXE              ${BXE_WEB_USERNAME}    ${BXE_Web_PASSWORD}    ${true}
    Enter Advanced Users
    Enter Site Manager

Select Location Information
    Click Element                    ${G_HOME_ADVANCEDACCESS_SITEMANAGER_ARROW}
    Wait Until Element Is Visible    ${G_HOME_ADVANCEDACCESS_SITEMANAGER_DROPDOWNMENU_LOCATIONINFO}

    Click Element                    ${G_HOME_ADVANCEDACCESS_SITEMANAGER_DROPDOWNMENU_LOCATIONINFO}
    Delays For Page Ready            3
    Click Element                    ${G_HOME_ADVANCEDACCESS_SITEMANAGER_DROPDOWNMENU_LOCATIONINFO_CUSTOMER_SPAN}
    Delays For Page Ready            3

    Select Checkbox                  ${G_HOME_ADVANCEDACCESS_SITEMANAGER_DROPDOWNMENU_LOCATIONINFO_CUSTOMER_CHECKBOX}
    Delays For Page Ready
    Checkbox Should Be Selected      ${G_HOME_ADVANCEDACCESS_SITEMANAGER_DROPDOWNMENU_LOCATIONINFO_CUSTOMER_CHECKBOX}

    Select Checkbox                  ${G_HOME_ADVANCEDACCESS_SITEMANAGER_DROPDOWNMENU_LOCATIONINFO_CUSTOMER_LOCATION_CHECKBOX}
    Delays For Page Ready
    Checkbox Should Be Selected      ${G_HOME_ADVANCEDACCESS_SITEMANAGER_DROPDOWNMENU_LOCATIONINFO_CUSTOMER_LOCATION_CHECKBOX}

Change Location Name
    ${test_location_name}    Generate Random String  8  [NUMBERS]
    Set Global Variable                     ${test_location_name}   ${test_location_name}

    Clear Element Text                      ${G_HOME_ADVANCEDACCESS_SITEMANAGER_DROPDOWNMENU_LOCATIONINFO_CUSTOMER_LOCATION_INPUT_TEXT}
    Enter Text                              ${G_HOME_ADVANCEDACCESS_SITEMANAGER_DROPDOWNMENU_LOCATIONINFO_CUSTOMER_LOCATION_INPUT_TEXT}     ${test_location_name}
    Click Element Using JavaScript Xpath    ${G_HOME_ADVANCEDACCESS_SITEMANAGER_DROPDOWNMENU_LOCATIONINFO_CUSTOMER_LOCATION_APPLY_BUTTON}

    ${apply_message}                        Get Data                ${G_HOME_ADVANCEDACCESS_SITEMANAGER_DROPDOWNMENU_LOCATIONINFO_CUSTOMER_LOCATION_APPLY_MESSAGE}
    Should Contain                          ${apply_message}        Settings applied.

Verify Location Name
    Login BXE              ${BXE_WEB_USERNAME}    ${BXE_Web_PASSWORD}    ${true}
    Enter Battery Systems
    ${current_location_name}    Get Data                    ${G_HOME_BATTERYSYSTEMACCESS_STRING1_LOCATIONNAME}
    Should be Equal             ${current_location_name}    ${test_location_name}