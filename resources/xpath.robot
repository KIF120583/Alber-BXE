*** Variables ***

# Login Page
${G_LOGIN_USERNAME_TAG}               //input[@name="ctl00$MainContent$UserName"]
${G_LOGIN_USERNAME_INPUT_TEXT}        //input[@name="ctl00$MainContent$UserName"]
${G_LOGIN_PASSWORD_INPUT_TEXT}        //input[@name="ctl00$MainContent$Password"]
${G_LOGIN_FAIL_TEXT}                  //*[@id="AppMainContainer"]/div/div[4]/div
${G_LOGIN_FAIL_EMPTY_USERNAME_TEXT}   //*[@id="MainContent_UserNameRequired"]
${G_LOGIN_FAIL_EMPTY_PASSWORD_TEXT}   //*[@id="MainContent_PasswordRequired"]
${G_LOGIN_BUTTON}                     //input[@name="ctl00$MainContent$LoginButton"]


# The page buttons after login
${G_HOME_LOGIN_USERNAME}          //*[@id="tbUserInformation_lblLoggedUserName"]
${G_HOME_BATTERYSYSTEMACCESS}     //*[@id="imgBatterySystemAccess"]
${G_HOME_ADVANCEDACCESS}          //*[@id="imgAdvancedAccess"]

# BatterySystemAccess
${G_HOME_BATTERYSYSTEMACCESS_CHECK}     //*[@id="AppMainContainer"]/div[6]/div[2]
${G_HOME_BATTERYSYSTEMACCESS_STRING1}    //*[@id="ctl00_MainContent_rgSystemStatus_ctl00__0"]/td[5]/a
${G_HOME_BATTERYSYSTEMACCESS_STRING1_TITLE}    //*[@id="ctl00_MainContent_ucStringView_ucStringViewDetails_pnlVoltageChartsWrapper"]/ul/li/a/span/span[2]
${G_HOME_BATTERYSYSTEMACCESS_STRING1_CELL_1}   //*[@id="pnlVoltageCharts"]//*[contains(@id,"imctl00_MainContent_ucStringView_ucStringViewDetails_pnlVoltageChartsWrapper_i0_i0_radchartVoltage")]/area[1]
${G_HOME_BATTERYSYSTEMACCESS_STRING1_CELL_2}   //*[@id="pnlVoltageCharts"]//*[contains(@id,"imctl00_MainContent_ucStringView_ucStringViewDetails_pnlVoltageChartsWrapper_i0_i0_radchartVoltage")]/area[2]
${G_HOME_BATTERYSYSTEMACCESS_STRING1_CELL_3}   //*[@id="pnlVoltageCharts"]//*[contains(@id,"imctl00_MainContent_ucStringView_ucStringViewDetails_pnlVoltageChartsWrapper_i0_i0_radchartVoltage")]/area[3]

# Battery
${G_HOME_BATTERYSYSTEMACCESS_STRING1_CELL_VOLTAGE}    //*[@id="ctl00_MainContent_ucStringView_ucStringViewDetails_ucStringDetailSummaryVoltageLithium_pnlStringDetailSummary_i0_i0_lblCellID"]
${G_HOME_BATTERYSYSTEMACCESS_STRING1_LOCATIONNAME}    //*[@id="ctl00_MainContent_rgSystemStatus_ctl00__0"]/td[3]

# AdvancedAccess
${G_HOME_ADVANCEDACCESS_CHECK}     //*[@id="AppMainContainer"]/div/div[1]
${G_HOME_ADVANCEDACCESS_SITEMANAGER}    //*[@id="ctl00_MainContent_pnlAdvancedAccess_i0_i0_lnkOptionalParametersManager"]

# SiteManager
${G_HOME_ADVANCEDACCESS_SITEMANAGER_TITLE}    //*[@id="MainContent_pnlTitle"]
${G_HOME_ADVANCEDACCESS_SITEMANAGER_ARROW}    //*[@id="ctl00_MainContent_RcbSiteManagerSelect_Arrow"]
${G_HOME_ADVANCEDACCESS_SITEMANAGER_DROPDOWNMENU_LOCATIONINFO}    //*[@id="ctl00_MainContent_RcbSiteManagerSelect_DropDown"]/div/ul/li[5]
${G_HOME_ADVANCEDACCESS_SITEMANAGER_DROPDOWNMENU_LOCATIONINFO_CUSTOMER_SPAN}    //*[@id="ctl00_MainContent_pnlSystemTreeView_i0_i0_tvSystem"]/ul/li/div/span[2]
${G_HOME_ADVANCEDACCESS_SITEMANAGER_DROPDOWNMENU_LOCATIONINFO_CUSTOMER_CHECKBOX}    //*[@id="ctl00_MainContent_pnlSystemTreeView_i0_i0_tvSystem"]/ul/li/div/label/input
${G_HOME_ADVANCEDACCESS_SITEMANAGER_DROPDOWNMENU_LOCATIONINFO_CUSTOMER_LOCATION_CHECKBOX}    //*[@id="ctl00_MainContent_pnlSystemTreeView_i0_i0_tvSystem"]/ul/li/ul/li/div/label/input
${G_HOME_ADVANCEDACCESS_SITEMANAGER_DROPDOWNMENU_LOCATIONINFO_CUSTOMER_LOCATION_INPUT_TEXT}    //*[@id="ctl00_MainContent_RpbLocation_i0_TxtLILocationName"]
${G_HOME_ADVANCEDACCESS_SITEMANAGER_DROPDOWNMENU_LOCATIONINFO_CUSTOMER_LOCATION_APPLY_BUTTON}    //*[@id="ctl00_MainContent_RpbLocation_i0_BtnLIApply_input"]
${G_HOME_ADVANCEDACCESS_SITEMANAGER_DROPDOWNMENU_LOCATIONINFO_CUSTOMER_LOCATION_APPLY_MESSAGE}    //*[@id="ctl00_MainContent_RpbLocation_i0_LblLIResult"]

# Title bar
${G_HOME_BUTTON}    //*[@id="tbUserInformation_lblTrail"]/a
${G_HOME_LOGOUT_BUTTON}    //*[@id="ctl00_tbUserInformation_rmTools"]/ul/li[1]
