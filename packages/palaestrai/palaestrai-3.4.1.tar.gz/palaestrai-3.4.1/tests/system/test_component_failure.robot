*** Settings ***
Documentation   Test handling of component failures
...
...             These tests trigger failures in subsystems of palaestrai.
...             The framework should react in a graceful manner, i.e., shut
...             down all other, working components in a controlled fashion,
...             give diagnostic output, and exit.

Library         Process
Library         OperatingSystem
Suite Teardown  Clean Files

*** Keywords ***
Clean Files
    Remove File                     ${TEMPDIR}${/}stdout.txt
    Remove File                     ${TEMPDIR}${/}stderr.txt
Log Result
    [Arguments]                     ${result_obj}
    IF                              ${result_obj}
        Log Many                        ${result_obj.stdout}    ${result_obj.stderr}
    END

*** Test Cases ***
Handle programming error in an environment
    Skip If                         1   "Skipped until the GSM is implemented."
    Append To Environment Variable  PYTHONPATH  ${CURDIR}${/}..
    ${ph} =                         Start Process       palaestrai      -vv     experiment-start    ${CURDIR}${/}..${/}fixtures${/}dying_environment_experiment.yml     stdout=${TEMPDIR}${/}stdout.txt     stderr=${TEMPDIR}${/}stderr.txt
    ${result} =                     Wait For Process    handle=${ph}    timeout=42s
    ${result2} =                    Wait For Process    handle=${ph}    timeout=5s          on_timeout=terminate
    Log Result                      ${result}
    Log Result                      ${result2}
    #Should Contain                  ${result.stdout}    Shinitai
    #Should Be True                  ${result} is not ${None}
