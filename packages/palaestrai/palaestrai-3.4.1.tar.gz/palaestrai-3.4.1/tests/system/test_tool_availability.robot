*** Settings ***
Documentation   The most basic system test possible
...
...             Runs cli and checks if it is available.

Library     OperatingSystem

*** Test Cases ***

Run palaestrai to catch renaming of the tool.
    ${rc}    ${output} =            Run and Return RC and Output    palaestrai --help
    Log                             ${output}
    Should Be Equal As Integers     ${rc}    0
