*** Settings ***
Documentation   Test handling of Ctrl+C (SIGINT)
...
...             This runs the system with the dummy experiment, but hits Ctrl+C after a short amount of time.
...             The test then monitors that everything exists smoothly.
...             There are several test cases that interrupt the running process after different amounts of time.

Library         Process
Library         OperatingSystem
Suite Teardown  Clean Files

*** Keywords ***
Clean Files
    Remove File                     ${TEMPDIR}${/}stdout.txt
    Remove File                     ${TEMPDIR}${/}stderr.txt

*** Test Cases ***
Interrupt palaestrai-experiment with the dummy test after 3 seconds.
    ${result} =                     Run Process  bash  ${CURDIR}/sigint_test_runner.sh  3  stdout=${TEMPDIR}${/}stdout.txt 	stderr=${TEMPDIR}${/}stderr.txt
    Log Many                        ${result.stdout}  ${result.stderr}
    ${match} =                      Should Match Regexp  ${result.stdout}  Executor\\([^)]+?\\) has received signal Signals.SIGINT, shutting down
    Should Be Equal As Integers     ${result.rc}  254

Interrupt palaestrai-experiment with the dummy test after 6 seconds.
    ${result} =                     Run Process  bash  ${CURDIR}/sigint_test_runner.sh  6  stdout=${TEMPDIR}${/}stdout.txt 	stderr=${TEMPDIR}${/}stderr.txt
    Log Many                        ${result.stdout}  ${result.stderr}
    ${match} =                      Should Match Regexp  ${result.stdout}  Executor\\([^)]+?\\) has received signal Signals.SIGINT, shutting down
    Should Be Equal As Integers     ${result.rc}  254

Interrupt palaestrai-experiment with the dummy test after 12 seconds.
    ${result} =                     Run Process  bash  ${CURDIR}/sigint_test_runner.sh  12  stdout=${TEMPDIR}${/}stdout.txt 	stderr=${TEMPDIR}${/}stderr.txt
    Log Many                        ${result.stdout}  ${result.stderr}
    ${match} =                      Should Match Regexp  ${result.stdout}  Executor\\([^)]+?\\) has received signal Signals.SIGINT, shutting down
    Should Be Equal As Integers     ${result.rc}  254
