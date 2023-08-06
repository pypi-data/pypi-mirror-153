*** Settings ***

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup   Run keywords  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***

Required field
    Enable autologin as  Manager
    Go to  ${PLONE_URL}/project_submission
    click button  Send
    Page Should Contain Element  css=dl.portalMessage.error

Elements submission
    Enable autologin as  Manager
    Go to  ${PLONE_URL}/project_submission
    Page should contain  Title
    Page should contain  Theme
    Page should contain  District
    Page should contain  Content
    Page should contain  Project image
