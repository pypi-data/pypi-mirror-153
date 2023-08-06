# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s cs.volto.publiccontracts -t test_contracts_folder.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src cs.volto.publiccontracts.testing.CS_VOLTO_PUBLICCONTRACTS_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/cs/volto/publiccontracts/tests/robot/test_contracts_folder.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a ContractsFolder
  Given a logged-in site administrator
    and an add ContractsFolder form
   When I type 'My ContractsFolder' into the title field
    and I submit the form
   Then a ContractsFolder with the title 'My ContractsFolder' has been created

Scenario: As a site administrator I can view a ContractsFolder
  Given a logged-in site administrator
    and a ContractsFolder 'My ContractsFolder'
   When I go to the ContractsFolder view
   Then I can see the ContractsFolder title 'My ContractsFolder'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add ContractsFolder form
  Go To  ${PLONE_URL}/++add++ContractsFolder

a ContractsFolder 'My ContractsFolder'
  Create content  type=ContractsFolder  id=my-contracts_folder  title=My ContractsFolder

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the ContractsFolder view
  Go To  ${PLONE_URL}/my-contracts_folder
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a ContractsFolder with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the ContractsFolder title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
