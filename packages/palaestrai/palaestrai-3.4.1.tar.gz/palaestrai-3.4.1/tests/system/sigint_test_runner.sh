#!/bin/bash

set -eux
timeout=${1:-3}

echo "Current directory: $(pwd)"

palaestrai -vv experiment-start ./tests/fixtures/dummy_run.yml &
pid=$!
sleep "$timeout"
kill -INT $pid
wait $pid
exit $?