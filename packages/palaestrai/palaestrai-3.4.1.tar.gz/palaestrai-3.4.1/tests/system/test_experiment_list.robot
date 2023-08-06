*** Settings ***
Documentation   Check provided database for run experiments.
...

Library         Process
Library         OperatingSystem
Suite Teardown  Clean Files

*** Keywords ***
Clean Files
    Remove File                     ${TEMPDIR}${/}stdout.txt
    Remove File                     ${TEMPDIR}${/}stderr.txt

*** Test Cases ***
Check dummy experiment database for experiment tables.
    ${result} =                     Run Process         palaestrai     experiment-list     --database     sqlite:///${CURDIR}${/}..${/}fixtures${/}dummy_database.db    stdout=${TEMPDIR}${/}stdout.txt 	stderr=${TEMPDIR}${/}stderr.txt
    Log Many                        ${result.stdout}    ${result.stderr}
    Should Be Equal As Integers     ${result.rc}   0
