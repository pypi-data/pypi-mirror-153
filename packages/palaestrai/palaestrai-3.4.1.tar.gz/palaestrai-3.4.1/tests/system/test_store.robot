*** Settings ***
Documentation   Test results store
...
...             This is a system test that runs the store setup, store migrations, and a dummy experiment
...             to check whether the store works and receives data.

Library         String
Library         Process
Library         OperatingSystem
Library         ${CURDIR}${/}ConfigFileModifier.py
Suite Teardown  Clean Files
Suite Setup     Create Config Files

*** Keywords ***
Clean Files
    Remove File                     ${TEMPDIR}${/}stdout*.txt
    Remove File                     ${TEMPDIR}${/}stderr*.txt
    Remove File                     ${TEMPDIR}${/}palaestrai.db
    remove file                     ${TEMPDIR}${/}palaestrai-default-runtime.conf.yml
    Remove File                     ${TEMPDIR}${/}store-test.conf.yml
    Remove File                     ${TEMPDIR}${/}store-test-sqlite.yml

Create Config Files
    ${result} =                     Run Process   palaestrai    runtime-config-show-default     stdout=${TEMPDIR}${/}palaestrai-default-runtime.conf.yml

Setup PostgreSQL Database Connection
    ${POSTGRES_DB} =                Get Environment Variable    POSTGRES_DB     ${EMPTY}
    Skip If                         "${POSTGRES_DB}" == ""   Skipping DB test because POSTGRES_* environment variables are unset
    ${r} =                          generate random string
    Set Environment Variable        PGDB    %{POSTGRES_DB}_${r}
    prepare_for_store_test          ${TEMPDIR}${/}palaestrai-default-runtime.conf.yml  ${TEMPDIR}${/}store-test.conf.yml
    Log File                        ${TEMPDIR}${/}store-test.conf.yml
    Set Environment Variable        PGPASSWORD      %{POSTGRES_PASSWORD}
    ${result} =                     Run Process     psql    -a  -c  DROP DATABASE IF EXISTS %{PGDB};  -h  %{POSTGRES_HOST}    -U    %{POSTGRES_USER}    postgres
    ${result} =                     Run Process     psql    -a  -c  CREATE DATABASE %{PGDB} WITH OWNER %{POSTGRES_USER}  -h  %{POSTGRES_HOST}    -U     %{POSTGRES_USER}   postgres
    Log Many                        ${result.stdout}    ${result.stderr}
    Should Be Equal As Integers     ${result.rc}    0

Drop PostgreSQL Database
    ${POSTGRES_DB} =                Get Environment Variable    POSTGRES_DB     ${EMPTY}
    Skip If                         "${POSTGRES_DB}" == ""   Skipping DB test because POSTGRES_* environment variables are unset
    ${result} =                     Run Process     psql    -a  -c  DROP DATABASE %{PGDB}  -h  %{POSTGRES_HOST}    -U     %{POSTGRES_USER}   postgres
    log many                        ${result.stdout}    ${result.stderr}
    Should Be Equal As Integers     ${result.rc}    0

*** Test Cases ***
Create database
    [Setup]                         setup postgresql database connection
    [Teardown]                      Drop PostgreSQL Database
    ${result} =                     Run Process   palaestrai    -c  ${TEMPDIR}${/}store-test.conf.yml   database-create
    Log Many                        ${result.stdout}    ${result.stderr}
    Should Be Equal As Integers     ${result.rc}    0
    ${result} =                     Run Process     psql  -a  -c  SELECT * FROM pg_tables;  -h  %{POSTGRES_HOST}    -U  %{POSTGRES_USER}    -A    -F    ,     %{PGDB}
    log many                        ${result.stdout}    ${result.stderr}
    Should Be Equal As Integers     ${result.rc}    0
    Should Contain                  ${result.stdout}    ,experiments,
    Should Contain                  ${result.stdout}    ,experiment_runs,
    Should Contain                  ${result.stdout}    ,experiment_run_instances,
    Should Contain                  ${result.stdout}    ,experiment_run_phases,
    Should Contain                  ${result.stdout}    ,environments,
    Should Contain                  ${result.stdout}    ,world_states,
    Should Contain                  ${result.stdout}    ,agents,
    Should Contain                  ${result.stdout}    ,brain_states,
    Should Contain                  ${result.stdout}    ,muscle_actions,

Verify TimescaleDB Hypertables
    [Setup]                         setup postgresql database connection
    [Teardown]                      Drop PostgreSQL Database
    ${result} =                     Run Process   palaestrai  -vv  -c  ${TEMPDIR}${/}store-test.conf.yml   database-create    stdout=${TEMPDIR}/stdout.txt 	stderr=${TEMPDIR}/stderr.txt
    Log Many                        ${result.stdout}    ${result.stderr}
    Should Be Equal As Integers     ${result.rc}    0
    ${result} =                     Run Process     psql  -a  -c  SELECT * FROM pg_extension;  -h  %{POSTGRES_HOST}    -U  %{POSTGRES_USER}    -A     -F  ,     %{PGDB}
    Log Many                        ${result.stdout}    ${result.stderr}
    Should Be Equal As Integers     ${result.rc}    0
    Should Contain                  ${result.stdout}    ,timescaledb,
    ${result} =                     Run Process     psql  -a  -c  SELECT table_name FROM _timescaledb_catalog.hypertable;  -h  %{POSTGRES_HOST}    -U  %{POSTGRES_USER}    -A     -F  ,     %{PGDB}
    log many                        ${result.stdout}    ${result.stderr}
    Should Be Equal As Integers     ${result.rc}    0
    Should Contain                  ${result.stdout}    world_states
    Should Contain                  ${result.stdout}    muscle_actions

Run dummy experiment and check for data
    [Timeout]                       180
    [Setup]                         setup postgresql database connection
    [Teardown]                      Drop PostgreSQL Database
    ${result} =                     Run Process   palaestrai  -c  ${TEMPDIR}${/}store-test.conf.yml   database-create    stdout=${TEMPDIR}/stdout.txt 	stderr=${TEMPDIR}/stderr.txt
    Log Many                        ${result.stdout}    ${result.stderr}
    Should Be Equal As Integers     ${result.rc}    0
    ${result} =                     Run Process   palaestrai  -c  ${TEMPDIR}${/}store-test.conf.yml   experiment-start    ${CURDIR}${/}..${/}fixtures${/}dummy_run.yml    stdout=${TEMPDIR}/stdout.txt 	stderr=${TEMPDIR}/stderr.txt
    Log Many                        ${result.stdout}    ${result.stderr}
    Should Be Equal As Integers     ${result.rc}    0
    ${result} =                     Run Process     psql  -a  -c  SELECT * FROM experiments;  -h  %{POSTGRES_HOST}    -U  %{POSTGRES_USER}    -A  -F  ,     %{PGDB}
    Log Many                        ${result.stdout}    ${result.stderr}
    Should Be Equal As Integers     ${result.rc}    0

Run multi-phase multi-agent dummy experiment and check for data
    [Timeout]                       270
    [Setup]                         setup postgresql database connection
    [Teardown]                      Drop PostgreSQL Database
    ${result} =                     Run Process   palaestrai  -c  ${TEMPDIR}${/}store-test.conf.yml   database-create    stdout=${TEMPDIR}/stdout.txt 	stderr=${TEMPDIR}/stderr.txt
    Log Many                        ${result.stdout}    ${result.stderr}
    Should Be Equal As Integers     ${result.rc}    0
    ${result} =                     Run Process  palaestrai  -c  ${TEMPDIR}${/}store-test.conf.yml  experiment-start  ${CURDIR}${/}..${/}fixtures${/}three_phases_four_agents_run.yml  stdout=${TEMPDIR}/stdout.txt  stderr=${TEMPDIR}/stderr.txt
    Log Many                        ${result.stdout}    ${result.stderr}
    Should Be Equal As Integers     ${result.rc}    0
    ${result} =                     Run Process  psql  -a  -c  SELECT * FROM experiments;  -h  %{POSTGRES_HOST}    -U  %{POSTGRES_USER}    -A  -F  ,     %{PGDB}
    Log Many                        ${result.stdout}    ${result.stderr}
    Should Be Equal As Integers     ${result.rc}    0
    ${result} =                     Run Process  psql  -a  -c  SELECT * FROM experiment_run_phases;  -h  %{POSTGRES_HOST}  -U  %{POSTGRES_USER}  -A  -F,  %{PGDB}
    Log Many                        ${result.stdout}  ${result.stderr}
    Should Contain                  ${result.stdout}  ,0,
    Should Contain                  ${result.stdout}  ,1,
    Should Contain                  ${result.stdout}  ,2,
    Should Be Equal As Integers     ${result.rc}  0

Test creation of SQLite database
    [Timeout]                       30
    ${result} =                     Run Process   palaestrai    runtime-config-show-default     stdout=${TEMPDIR}${/}store-test-sqlite.yml
    ${db_file_path} =               prepare_for_sqlite_store_test   ${TEMPDIR}${/}store-test-sqlite.yml    ${TEMPDIR}${/}store-test-sqlite.yml     ${TEMPDIR}
    Log                             SQLite store runtime configuration file created at: ${TEMPDIR}${/}store-test-sqlite.yml
    ${result} =                     Run Process   palaestrai    -c  ${TEMPDIR}${/}store-test-sqlite.yml   database-create   stdout=${TEMPDIR}${/}stdout.txt 	stderr=${TEMPDIR}${/}stderr.txt
    Log Many                        ${result.stdout}    ${result.stderr}
    Should Be Equal As Integers     ${result.rc}    0
    File Should Exist               ${db_file_path}
    ${result} =                     Run Process     sqlite3     ${db_file_path}     .dump
    Should Contain                  ${result.stdout}    CREATE TABLE world_states
    Remove File                     ${db_file_path}

Run dummy experiment with SQLite and check for data
    [Timeout]                       240
    ${result} =                     Run Process   palaestrai    runtime-config-show-default     stdout=${TEMPDIR}${/}store-test-sqlite.yml
    ${db_file_path} =               prepare_for_sqlite_store_test   ${TEMPDIR}${/}store-test-sqlite.yml    ${TEMPDIR}${/}store-test-sqlite.yml      ${TEMPDIR}
    log                             SQLite store runtime configuration file created at: ${TEMPDIR}${/}store-test-sqlite.yml
    Log File                        ${TEMPDIR}${/}store-test-sqlite.yml
    ${result} =                     Run Process   palaestrai    -c  ${TEMPDIR}${/}store-test-sqlite.yml   database-create   stdout=${TEMPDIR}${/}stdout.txt     stderr=${TEMPDIR}${/}stderr.txt
    log many                        ${result.stdout}    ${result.stderr}
    Should Be Equal As Integers     ${result.rc}    0
    File Should Exist               ${db_file_path}
    ${result} =                     Run Process   sqlite3    ${db_file_path}   .dump     	stdout=${TEMPDIR}${/}stdout-sqlitedump.txt    stderr=${TEMPDIR}/stderr-sqlite3dump.txt
    Log Many                        ${result.stdout}    ${result.stderr}
    start process                   palaestrai    -c  ${TEMPDIR}${/}store-test-sqlite.yml   experiment-start    ${CURDIR}${/}..${/}fixtures${/}dummy_run.yml   stdout=${TEMPDIR}/stdout-sqlite3dummy.txt 	stderr=${TEMPDIR}/stderr-sqlite3dummy.txt
    ${result} =                     Wait For Process  timeout=180  on_timeout=kill
    Log Many                        ${result.stdout}    ${result.stderr}
    Should Be Equal As Integers     ${result.rc}    0
    File Should Exist               ${db_file_path}
    ${result} =                     Run Process     sqlite3     ${db_file_path}     SELECT COUNT(*) FROM experiments;
    log many                        ${result.stdout}    ${result.stderr}
    Should Be Equal As Integers     ${result.rc}    0
    Should Not Be Equal As Strings  ${result.stdout}    0

Running without store should be possible, but emit a warning
    [Timeout]                       180
    ${result} =                     Run Process   palaestrai    -c  ${CURDIR}${/}..${/}fixtures${/}palaestrai-runtime-nostore.conf.yaml   experiment-start    ${CURDIR}${/}..${/}fixtures${/}dummy_run.yml   stdout=${TEMPDIR}/stdout.txt 	stderr=${TEMPDIR}/stderr.txt
    Log Many                        ${result.stdout}    ${result.stderr}
    Should Be Equal As Integers     ${result.rc}    0
    Should Contain                  ${result.stdout}     has no store_uri configured, I'm going to disable myself.

Failing to store should be handled gracefully
    [Timeout]                       180
    ${result} =                     Run Process   palaestrai    runtime-config-show-default
    Create File                     ${TEMPDIR}${/}store-test-sqlite.yml    ${result.stdout}
    ${db_file_path} =               prepare_for_sqlite_store_test   ${TEMPDIR}${/}store-test-sqlite.yml    ${TEMPDIR}${/}store-test-sqlite.yml      ${TEMPDIR}
    log                             SQLite store runtime configuration file created at: ${TEMPDIR}${/}store-test-sqlite.yml
    Remove File                     ${db_file_path}
    ${result} =                     Run Process   palaestrai    -c  ${TEMPDIR}${/}store-test-sqlite.yml   experiment-start    ${CURDIR}${/}..${/}fixtures${/}dummy_run.yml    stdout=${TEMPDIR}/stdout.txt 	stderr=${TEMPDIR}/stderr.txt
    log many                        ${result.stdout}    ${result.stderr}
    Should Be Equal As Integers     ${result.rc}    0
    Should Contain                  ${result.stdout}     puny experiment

Use store to analyze a dummy-experiment
    Start Process                   jupyter  nbconvert  --to  html  --execute  ${CURDIR}${/}store_example_analysis.ipynb  stdout=${TEMPDIR}${/}stdout.txt  stderr=${TEMPDIR}${/}stderr.txt
    ${result} =                     Wait For Process  timeout=180  on_timeout=kill
    Log Many                        ${result.stdout}    ${result.stderr}
    Should Be Equal As Integers     ${result.rc}   0
    File Should Exist               ${CURDIR}${/}store_example_analysis.html

End-to-End Store test
    [Timeout]                       240
    ${result} =                     Run Process   palaestrai    runtime-config-show-default     stdout=${TEMPDIR}${/}store-test-sqlite.yml
    ${db_file_path} =               prepare_for_sqlite_store_test   ${TEMPDIR}${/}store-test-sqlite.yml    ${TEMPDIR}${/}store-test-sqlite.yml      ${TEMPDIR}
    log                             SQLite store runtime configuration file created at: ${TEMPDIR}${/}store-test-sqlite.yml
    Log File                        ${TEMPDIR}${/}store-test-sqlite.yml
    ${result} =                     Run Process   palaestrai    -c  ${TEMPDIR}${/}store-test-sqlite.yml   database-create   stdout=${TEMPDIR}${/}stdout.txt     stderr=${TEMPDIR}${/}stderr.txt
    Log Many                        ${result.stdout}    ${result.stderr}
    Should Be Equal As Integers     ${result.rc}    0
    File Should Exist               ${db_file_path}
    ${pythonpath} =                 Get Environment Variable  PYTHONPATH  default=""
    Set Environment Variable        PYTHONPATH  ${pythonpath}:${CURDIR}${/}..
    Start Process                   palaestrai  -c  ${TEMPDIR}${/}store-test-sqlite.yml   experiment-start    ${CURDIR}${/}..${/}fixtures${/}end_to_end_test_run.yml  stdout=${TEMPDIR}/stdout-sqlite3dummy.txt  stderr=${TEMPDIR}/stderr-sqlite3dummy.txt
    ${result} =                     Wait For Process  timeout=180  on_timeout=kill
    Log Many                        ${result.stdout}    ${result.stderr}
    Should Be Equal As Integers     ${result.rc}  0
    ${check_sql} =                  Get File  ${CURDIR}${/}end_to_end_reward.sql
    ${result} =                     Run Process   sqlite3  -csv  ${db_file_path}  ${check_sql}  stdout=${TEMPDIR}${/}stdout-sqlitedump.txt  stderr=${TEMPDIR}/stderr-sqlite3dump.txt
    Log Many                        ${result.stdout}  ${result.stderr}
    Remove File                     ${db_file_path}
    Should Not Match Regexp         ${result.stdout}  (?m)0,$
