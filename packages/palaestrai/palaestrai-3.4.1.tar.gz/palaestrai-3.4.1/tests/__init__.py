import os

_file_dir = os.path.dirname(os.path.realpath(__file__))
dummy_exp_path: str = os.path.abspath(
    f"{_file_dir}/fixtures/dummy_experiment.yml"
)
runtime_path: str = os.path.abspath(
    f"{_file_dir}/fixtures/palaestrai-runtime-debug.conf.yaml"
)
