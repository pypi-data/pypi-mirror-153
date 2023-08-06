*** Settings ***
Documentation   Test experiment syntax check CLI
...
...             The palaestrAI CLI offers an option to syntax-check
...             experiment run definition files. This test case verifies that
...             the various ways offered by a CLI to do so work.

Library         Process
Library         OperatingSystem
Suite Teardown  Clean Files

*** Keywords ***
Clean Files
    Remove File                     ${TEMPDIR}${/}stdout.txt
    Remove File                     ${TEMPDIR}${/}stderr.txt

*** Test Cases ***
Test simple file without errors
    [Teardown]                      Clean Files
    ${result} =                     Run Process    palaestrai  experiment-check-syntax    ${CURDIR}${/}..${/}fixtures${/}dummy_run.yml    stdout=${TEMPDIR}${/}stdout.txt    stderr=${TEMPDIR}${/}stderr.txt
    Log Many                        ${result.stdout}    ${result.stderr}
    Should Be Equal As Integers     ${result.rc}    0
    Should Not Contain              ${result.stderr}    contain errors:

Test simple file containing errors
    [Teardown]                      Clean Files
    ${result} =                     Run Process    palaestrai  experiment-check-syntax    ${CURDIR}${/}..${/}fixtures${/}invalid_run.yml    stdout=${TEMPDIR}${/}stdout.txt    stderr=${TEMPDIR}${/}stderr.txt
    Log Many                        ${result.stdout}    ${result.stderr}
    Should Be Equal As Integers     ${result.rc}    1
    Should Contain                  ${result.stderr}    contain errors:

Test multiple files
    [Teardown]                      Clean Files
    ${result} =                     Run Process    palaestrai  experiment-check-syntax    ${CURDIR}${/}..${/}fixtures${/}dummy_run.yml    ${CURDIR}${/}..${/}fixtures${/}invalid_run.yml    stdout=${TEMPDIR}${/}stdout.txt    stderr=${TEMPDIR}${/}stderr.txt
    Log Many                        ${result.stdout}    ${result.stderr}
    Should Be Equal As Integers     ${result.rc}    1
    Should Contain                  ${result.stderr}    contain errors:
    Should Contain                  ${result.stderr}    invalid_run.yml
    Should Not Contain              ${result.stderr}    dummy_run.yml

Test syntax check from STDIN
    [Teardown]                      Clean Files
    ${result} =                     Run Process    cat  ${CURDIR}${/}..${/}fixtures${/}invalid_run.yml  |   palaestrai  experiment-check-syntax     -        stdout=${TEMPDIR}${/}stdout.txt    stderr=${TEMPDIR}${/}stderr.txt  shell=True
    Log Many                        ${result.stdout}    ${result.stderr}
    Should Be Equal As Integers     ${result.rc}    1
    Should Contain                  ${result.stderr}    contain errors:
