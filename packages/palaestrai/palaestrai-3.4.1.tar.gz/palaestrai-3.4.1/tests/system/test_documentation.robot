*** Settings ***
Documentation    Build the documentation and checks for document sanity

Library         Process
Library         OperatingSystem
Library         tempfile

Test Setup      Create Tempdir
Test Teardown   Cleanup Tempdir

*** Keywords ***
Create Tempdir
    ${sphinx_out_dir} =             tempfile.mkdtemp  dir=${TEMPDIR}
    Set Environment Variable        sphinx_out_dir  ${sphinx_out_dir}

Cleanup Tempdir
    Remove Directory                %{sphinx_out_dir}  recursive=True

*** Test Cases ***
Sphinx build
    ${result} =                     Run Process  sphinx-build  -v  -a   ${CURDIR}${/}..${/}..${/}doc  %{sphinx_out_dir}  stdout=${TEMPDIR}${/}stdout.txt  stderr=${TEMPDIR}${/}stderr.txt
    Log Many                        ${result.stdout}  ${result.stderr}
    Should Be Equal As Integers     ${result.rc}  0
    File Should Exist               %{sphinx_out_dir}${/}index.html

ER Diagram Generation
    ${result} =                     Run Process  sphinx-build  -v  -a  ${CURDIR}${/}..${/}..${/}doc  %{sphinx_out_dir}  stdout=${TEMPDIR}${/}stdout.txt  stderr=${TEMPDIR}${/}stderr.txt
    Log Many                        ${result.stdout}  ${result.stderr}
    Should Be Equal As Integers     ${result.rc}  0
    File Should Exist               %{sphinx_out_dir}${/}_images${/}store_er_diagram.png
