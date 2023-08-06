import os
import random
import string
from pathlib import Path

from ruamel.yaml import YAML

yaml = YAML(typ="safe")
POSTGRES_ENVIRONMENT_VARIABLES = {
    "POSTGRES_HOST",
    "POSTGRES_USER",
    "POSTGRES_PASSWORD",
    "PGDB",
}


def prepare_for_store_test(source_path, target_path):
    conf = yaml.load(Path(source_path))
    rewrite_config = all(
        k in os.environ for k in POSTGRES_ENVIRONMENT_VARIABLES
    )
    if rewrite_config:
        conf["store_uri"] = "postgresql://%s:%s@%s/%s" % (
            os.environ["POSTGRES_USER"],
            os.environ["POSTGRES_PASSWORD"],
            os.environ["POSTGRES_HOST"],
            os.environ["PGDB"],
        )
        conf["logging"]["loggers"]["palaestrai.store"]["level"] = "DEBUG"
    with open(target_path, "w") as fp:
        yaml.dump(conf, fp)


def prepare_for_sqlite_store_test(source_path, target_path, tmpdir):
    conf = yaml.load(Path(source_path))
    print(source_path)
    print(conf)
    assert conf
    db_file_name = "".join(
        random.choices(string.ascii_uppercase + string.digits, k=12)
    )
    db_file_path = "%s/palaestrai-%s.db" % (tmpdir, db_file_name)
    conf["store_uri"] = "sqlite:///%s" % db_file_path
    conf["logging"]["loggers"]["palaestrai.store"]["level"] = "DEBUG"
    with open(target_path, "w") as fp:
        yaml.dump(conf, fp)
    return db_file_path
