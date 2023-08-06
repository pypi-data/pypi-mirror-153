*** Settings ***
Documentation   The most basic system test possible
...
...             This system test serves as the most basic test for the whole
...             ARL core system. It exists to ensure that the infrastructure
...             code works, i.e., that we can run `arlctl', get help,
...             or see debugging output.

Library         OperatingSystem
Library         Process
Suite Teardown  Clean Files

*** Keywords ***
Clean Files
    Remove File                     ${TEMPDIR}${/}stdout.txt
    Remove File                     ${TEMPDIR}${/}stderr.txt

*** Test Cases ***
Run palaestrai executable to display help
    ${rc}    ${output} =            Run and Return RC and Output    palaestrai --help
    Log                             ${output}
    Should Be Equal As Integers     ${rc}    0

Ensure an explicitly given config file is loaded
    File Should Exist               ./tests/fixtures/palaestrai-runtime-debug.conf.yaml
    ${result} =                     Run Process     palaestrai   -c     ./tests/fixtures/palaestrai-runtime-debug.conf.yaml     runtime-config-show-effective    stdout=${TEMPDIR}${/}stdout.txt     stderr=${TEMPDIR}${/}stderr.txt
    Log Many                        ${result.stdout}    ${result.stderr}
    Should Be Equal As Integers     ${result.rc}    0
    ${match} =                      Should Match Regexp    ${result.stdout}         Configuration loaded from: .*?/tests/fixtures/palaestrai-runtime-debug.conf.yaml
