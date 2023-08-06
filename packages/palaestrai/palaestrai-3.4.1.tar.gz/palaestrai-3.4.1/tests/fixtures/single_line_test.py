#!/usr/bin/env python3

import sys
import palaestrai
from palaestrai.experiment import ExecutorState


if __name__ == "__main__":
    _, executor_final_state = palaestrai.execute(sys.argv[1])
    if executor_final_state != ExecutorState.EXITED:
        sys.exit(
            {
                ExecutorState.SIGINT: -2,
                ExecutorState.SIGABRT: -6,
                ExecutorState.SIGTERM: -15,
            }[executor_final_state]
        )
