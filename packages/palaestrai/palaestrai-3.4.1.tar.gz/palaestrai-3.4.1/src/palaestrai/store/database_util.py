import time

from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError, OperationalError
from sqlalchemy.sql.expression import text
from sqlalchemy_utils import database_exists, create_database

from . import LOG
from .database_model import Model

# Default chunk_time_interval. Might become configurable at some point iff we
# decide to keep TimescaleDB.
TIMESCALEDB_DEFAULT_CHUNK_SIZE_INTERVAL = 512


def _create_timescaledb_extension(engine):
    with engine.begin() as conn:
        conn.execute("CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;")
    timescale_tables = {
        "world_states",
        "muscle_actions",
    }
    with engine.begin() as conn:
        for tbl in timescale_tables:
            cmd = (
                f"SELECT * FROM create_hypertable("
                f"'{tbl}', "  # Table name
                f"'id', "  # Primary partitioning column
                f"chunk_time_interval => "
                f"{TIMESCALEDB_DEFAULT_CHUNK_SIZE_INTERVAL})"
            )
            res = conn.execute(text(cmd))
            LOG.debug(
                'Result of executing "%s" during setup: %s',
                cmd,
                res.fetchall(),
            )
            res.close()
    LOG.info(
        "Created TimescaleDB hypertables: %s, set 'chunk_time_interval' "
        "parameter to %d. HINT: The chunk_time_interval should be chosen such "
        "that all active chunks of all your hypertables fit in 25% of your "
        "RAM. You can change the value with TimescaleDB's "
        "set_chunk_time_interval() function.",
        ", ".join(timescale_tables),
        TIMESCALEDB_DEFAULT_CHUNK_SIZE_INTERVAL,
    )


def setup_database(uri):
    """Creates the database from the current model in one go.

    :param uri: The complete database connection URI.
    """
    engine = create_engine(uri)
    while not database_exists(uri):
        i = 1
        if i > 3:  # Hardcoded max tries. No real reason to configure this.
            LOG.critical(
                "Could not create the database. See errors above for more "
                "details. Giving up now."
            )
            raise RuntimeError("Could not create database")
        try:
            create_database(uri)
        except OperationalError as e:
            try:
                import psycopg2.errors

                if isinstance(e.orig, psycopg2.errors.ObjectInUse):
                    LOG.warning(
                        "Could not create database because the template was "
                        "in use. Retrying in %d seconds.",
                        i,
                    )
                    time.sleep(i)
                else:
                    break
            except ImportError:
                pass
        except ProgrammingError as e:
            LOG.error(
                "There was an error creating the database. I will continue "
                "and hope for the best. The error was: %s",
                e,
            )
        i += 1

    with engine.begin() as conn:
        try:
            Model.metadata.create_all(engine)
        except ProgrammingError as e:
            LOG.error("Could not create database: %s" % e)
            raise e
    try:
        _create_timescaledb_extension(engine)
    except OperationalError as e:
        LOG.warning(
            "Could not create extension timescaledb and create hypertables: "
            "%s. "
            "Your database setup might lead to noticeable slowdowns with "
            "larger experiment runs. Please upgrade to PostgreSQL with "
            "TimescaleDB for the best performance." % e
        )
