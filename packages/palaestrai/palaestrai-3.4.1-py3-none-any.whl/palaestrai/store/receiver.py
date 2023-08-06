from __future__ import annotations

import inspect
import queue
import threading
import time
import uuid
import zlib
from typing import Dict, Tuple

from numpy.random import RandomState

import jsonpickle
import jsonpickle.ext.numpy as jsonpickle_numpy
import ruamel.yaml as yml

import sqlalchemy
import sqlalchemy.engine
import sqlalchemy.exc
import sqlalchemy.orm
from sqlalchemy import select, Text
from sqlalchemy.orm.attributes import flag_modified

import palaestrai.core.MDP as MDP
import palaestrai.core.protocol as proto
from palaestrai.core import RuntimeConfig
from palaestrai.core.serialisation import deserialize

from . import LOG
from . import database_model as dbm


class StoreReceiver(threading.Thread):
    """The message receiver of the palaestrAI store.

    The store hooks into the global communication, reading every message that
    is being exchanged between :class:`Executor`, :class:`RunGovernor`,
    :class:`AgentConductor`, :class:`Environment`, :class:`Brain`, and
    :class:`Muscle` instances. From these messages, it reads all relevant
    status information in order to relay them to the store database for later
    analysis of experiments.
    """

    def __init__(self, queue, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._queue = queue
        self._buffer = []
        self._running = True
        self._uid = uuid.uuid4()
        self._db_engine = None
        self._db_session_maker = None
        self._db_session = None
        self._db_connection_open = False
        self._message_dispatch = {
            v: None
            for k, v in proto.__dict__.items()
            if (
                inspect.isclass(v)
                and (k.endswith("Request") or k.endswith("Response"))
            )
        }
        self._message_dispatch.update(
            {
                proto.ExperimentRunStartRequest: self._write_experiment,
                proto.SimulationStartRequest: self._write_experiment_run_phase,
                proto.EnvironmentSetupResponse: self._write_environment,
                proto.EnvironmentStartResponse: None,
                proto.EnvironmentUpdateResponse: self._write_world_state,
                proto.AgentSetupRequest: self._write_agent,
                proto.AgentSetupResponse: self._write_muscles,
                proto.AgentUpdateRequest: self._write_agent_inputs,
                proto.AgentUpdateResponse: self._write_agent_actions,
                proto.SimulationControllerTerminationResponse: self._invalidate_cache,
            }
        )
        try:
            self._store_uri = RuntimeConfig().store_uri
            if not self._store_uri:
                raise KeyError
        except KeyError:
            LOG.error(
                "StoreReceiver(id=%0xd, uid=%s) "
                "has no store_uri configured, I'm going to disable myself. :-("
                " If you want to employ me, set the 'store_uri' runtime "
                "configuration parameter.",
                id(self),
                self._uid,
            )
            self.disable()
        jsonpickle_numpy.register_handlers()
        jsonpickle.set_preferred_backend("simplejson")
        jsonpickle.set_encoder_options("simplejson", ignore_nan=True)

        # Cache to avoid lookup queries:
        self._last_known_muscle_actions = {}
        self._environment_ticks: Dict[Tuple, int] = {}
        self._known_agents: Dict[Tuple, dbm.Agent] = {}
        self._known_environments: Dict[Tuple, dbm.Environment] = {}

    def disable(self):
        """Disables the store completely."""
        for k in self._message_dispatch.keys():  # Disable all handlers.
            self._message_dispatch[k] = None
        if self._db_session:
            # Explicitly close session here or we will see "session used in
            # wrong thread" errors, because the garbage collector runs in a
            # different thread.
            self._db_session.close()
        self._db_session = None

    @property
    def uid(self):
        return self._uid

    @property
    def _dbh(self) -> sqlalchemy.orm.session:
        if self._db_session is None:
            self._db_engine = sqlalchemy.create_engine(
                RuntimeConfig().store_uri,
                json_serializer=jsonpickle.dumps,
                json_deserializer=jsonpickle.loads,
            )
            self._db_session_maker = sqlalchemy.orm.sessionmaker()
            self._db_session_maker.configure(bind=self._db_engine)
            try:
                self._db_session = self._db_session_maker()
                LOG.debug(
                    "StoreReceiver(id=%0xd, uid=%s) connected to: %s",
                    id(self),
                    self.uid,
                    RuntimeConfig().store_uri,
                )
            except (
                sqlalchemy.exc.OperationalError,
                sqlalchemy.exc.ArgumentError,
            ) as e:
                LOG.error(
                    "StoreReceiver(id=%0xd, uid=%s) "
                    "could not connect to %s: %s. "
                    "I'm going to say good-bye to this cruel world now!",
                    id(self),
                    self.uid,
                    RuntimeConfig().store_uri,
                    e,
                )
                self.disable()
        return self._db_session

    def run(self):
        """Run the store."""
        LOG.debug(
            "StoreReceiver(id=0x%x, uid=%s) revving the engines...",
            id(self),
            self._uid,
        )
        while (
            self._running or not self._queue.empty() or len(self._buffer) > 0
        ):
            while len(self._buffer) > 0:
                LOG.debug(
                    "StoreReceiver(id=%0xd, uid=%s) "
                    "tries to drain our buffer (len=%d).",
                    id(self),
                    self.uid,
                    len(self._buffer),
                )
                messages = self._buffer
                self._buffer = []
                while messages and len(self._buffer) == 0:
                    self.write(messages.pop(0))
                    if len(self._buffer) > 0:  # write unsuccessful
                        self._buffer += messages  # Store back the rest
                        time.sleep(1)
            try:
                msg = self._queue.get(timeout=1)
            except queue.Empty:
                time.sleep(1)
                continue
            msg_type, msg_uid, msg_obj = StoreReceiver._read(msg)
            LOG.debug(
                "%s received message: type=%s, uid=%s, payload=%s; queue "
                "size: %s",
                self,
                msg_type,
                msg_uid,
                msg_obj,
                self._queue.qsize(),
            )
            if msg_type in ("ignore", "error"):
                self._queue.task_done()
                continue
            if isinstance(msg_obj, list):
                LOG.info(
                    "StoreReceiver(id=0x%x, uid=%s) received a list of "
                    "%d messages. Handling all these messages separately.",
                    id(self),
                    self._uid,
                    len(msg_obj),
                )
                for msg in msg_obj:
                    self.write(msg)
            else:
                self.write(msg_obj)

            self._queue.task_done()
        self.disable()
        LOG.info("%s has shut down.", self)

    def shutdown(self):
        LOG.info(
            "%s prepares to shut down: waiting to process %s messages in the "
            "queue.",
            self,
            self._queue.qsize(),
        )
        self._running = False

    def write(self, message):
        """Main method called to write a message to the buffer."""
        if message.__class__ not in self._message_dispatch:
            StoreReceiver._handle_unknown_message(message)
            return
        if self._message_dispatch[message.__class__] is not None:
            try:
                LOG.debug(
                    "StoreReceiver(id=0x%x, uid=%s) dispatching message %s; "
                    "%d messages waiting",
                    id(self),
                    self.uid,
                    message,
                    self._queue.qsize(),
                )
                self._message_dispatch[message.__class__](message)
            except (
                sqlalchemy.exc.NoForeignKeysError,
                sqlalchemy.exc.ProgrammingError,
            ) as e:
                LOG.critical(
                    "StoreReceiver(id=0x%x, uid=%s) "
                    "notes that the developers are too stupid to get the "
                    "schema right: %s",
                    id(self),
                    self.uid,
                    e,
                )
                self.disable()
            except (
                sqlalchemy.exc.InvalidRequestError,
                sqlalchemy.exc.OperationalError,
                sqlalchemy.exc.ArgumentError,
            ) as e:
                if not self._db_connection_open:
                    LOG.critical(
                        "StoreReceiver(id=0x%x, uid=%s) "
                        "failed to write to the database: %s. "
                        "Please check that connecting to the database is "
                        "possible and that you have run `palaestrai "
                        "database-create'. I'm going to disable myself now. "
                        "Go on with your puny experiment, I can't keep track "
                        "of it!",
                        id(self),
                        self.uid,
                        e,
                    )
                    self.disable()
                else:
                    LOG.warning(
                        "StoreReceiver(id=0x%x, uid=%s) "
                        "failed to write to the database: %s."
                        "I will buffer the messages until the database "
                        "is available again and write them to the database "
                        "then.",
                        id(self),
                        self.uid,
                        e,
                    )
                    self._buffer.append(message)
                    LOG.debug(
                        "StoreReceiver(id=0x%x, uid=%s) "
                        "added message to the buffer. "
                        "Number of entries in the buffer is %d ",
                        id(self),
                        self.uid,
                        len(self._buffer),
                    )
            self._db_connection_open = True

    @staticmethod
    def _handle_unknown_message(message):
        LOG.warning(
            "Store received message %s, but cannot handle it - ignoring",
            message,
        )

    def _write_experiment(self, msg: proto.ExperimentRunStartRequest):
        from palaestrai.experiment.experiment_run import ExperimentRun

        dummy_experiment_name = (
            "Dummy Experiment record "
            "for ExperimentRun %s" % msg.experiment_run_id
        )
        query = select(dbm.Experiment).where(
            dbm.Experiment.name == dummy_experiment_name
        )
        experiment_hack_record = self._dbh.execute(query).scalars().first()
        if not experiment_hack_record:
            experiment_hack_record = dbm.Experiment(name=dummy_experiment_name)
            yaml = yml.YAML(typ="safe")
            yaml.register_class(ExperimentRun)
            yaml.representer.add_representer(
                RandomState, ExperimentRun.repr_randomstate
            )
            yaml.constructor.add_constructor(
                "rng", ExperimentRun.repr_randomstate
            )
            self._dbh.add(experiment_hack_record)

        query = select(dbm.ExperimentRun).where(
            dbm.ExperimentRun.uid == msg.experiment_run.uid
        )
        result = self._dbh.execute(query).scalars().all()
        if len(result) > 1:
            LOG.warning(
                "StoreReceiver(id=0x%x, uid=%s) "
                "found %d entries for ExperimentRun(uid=%s) "
                "when there should be at most one. I'm going to use the first "
                "one, but if strange things happen, don't blame it on me.",
                id(self),
                self.uid,
                len(result),
                msg.experiment_run_id,
            )
        try:
            experiment_run_record = result[0]
        except IndexError:
            experiment_run_record = dbm.ExperimentRun(
                uid=msg.experiment_run.uid,
                document=msg.experiment_run,
            )
            experiment_hack_record.experiment_runs.append(
                experiment_run_record
            )

        # Every time we see an ExperimentRunStartRequest, it means that we
        # also create a new instance of this run.

        try:
            experiment_run_record.experiment_run_instances.append(
                dbm.ExperimentRunInstance(
                    uid=msg.experiment_run.instance_uid,
                )
            )
            self._dbh.commit()
        except sqlalchemy.exc.IntegrityError as e:
            LOG.warning(
                "%s encountered a glitch in the Matrix: A record for "
                "ExperimentRunInstance(uid=%s) was already there! Perhaps "
                "your environment does not provide enough entropy, or we have "
                "a resend. I'm going to ignore this error and continue as "
                "best as I can. (%s)",
                self,
                msg.experiment_run.instance_uid,
                e,
            )

    def _write_experiment_run_phase(
        self, message: proto.SimulationStartRequest
    ):
        query = select(dbm.ExperimentRunInstance).where(
            dbm.ExperimentRunInstance.uid == message.experiment_run_instance_id
        )
        try:
            experiment_run_instance_record = (
                self._dbh.execute(query).scalars().one()
            )
        except sqlalchemy.orm.exc.NoResultFound:
            LOG.error(
                "%s received a %s, but could not find an instance of %s. "
                "I cannot store information about this phase; expect more "
                "errors ahead.",
                self,
                repr(message),
                message.experiment_run_instance_id,
            )
            return
        except sqlalchemy.orm.exc.MultipleResultsFound:
            LOG.error(
                "%s received a %s, "
                "but there was already an entry for it! I won't create a new "
                "one, but you might see more errors ahead.",
                self,
                repr(message),
            )
            return
        LOG.debug(
            "%s writing new ExperimentRunPhase for "
            "ExperimentRun(uid=%s, instance_uid=%s).",
            self,
            message.experiment_run_id,
            message.experiment_run_instance_id,
        )
        try:
            experiment_run_instance_record.experiment_run_phases.append(
                dbm.ExperimentRunPhase(
                    number=message.experiment_run_phase,
                    experiment_run_instance_id=experiment_run_instance_record.id,
                    uid=message.experiment_run_phase_id,
                    configuration=message.experiment_run_phase_configuration,
                    mode=message.experiment_run_phase_configuration.get(
                        "mode", None
                    ),
                )
            )
            self._dbh.commit()
        except sqlalchemy.exc.IntegrityError as e:
            LOG.debug(
                "%s saw a %s, but got an IntegrityError from the DB (%s). "
                "I assume a reset and will ignore this error.",
                self,
                repr(message),
                e,
            )

    def _write_environment(self, message: proto.EnvironmentSetupResponse):
        query = (
            sqlalchemy.select(
                dbm.ExperimentRunInstance, dbm.ExperimentRunPhase
            )
            .join(dbm.ExperimentRunInstance.experiment_run_phases)
            .where(
                dbm.ExperimentRunInstance.uid
                == message.experiment_run_instance_id,
                dbm.ExperimentRunPhase.number == message.experiment_run_phase,
            )
        )
        try:
            result = self._dbh.execute(query).one()
        except sqlalchemy.orm.exc.MultipleResultsFound:
            LOG.error(
                "StoreReceiver(id=0x%x, uid=%s) "
                "encountered an EnvironmentSetupResponse("
                "experiment_run_id=%s, experiment_run_instance_id=%s, "
                "experiment_run_phase=%s), "
                "but there are duplicate entries for this run phase. "
                "I will not record this environment as I do not know to which "
                "phase it belongs. "
                "Expect more errors from the store ahead.",
                id(self),
                self.uid,
                message.experiment_run_id,
                message.experiment_run_instance_id,
                message.experiment_run_phase,
            )
            return
        except sqlalchemy.orm.exc.NoResultFound:
            LOG.error(
                "%s encountered an %s, "
                "but there is no record of this phase in the store. "
                "I will not record this environment as I cannot do it; "
                "expect more errors from the store ahead.",
                self,
                repr(message),
            )
            return
        environment_records = result[dbm.ExperimentRunPhase].environments
        try:
            environment_record = dbm.Environment(
                uid=message.environment_id,
                type=message.environment_type,
                parameters=message.environment_parameters,
                environment_conductor_uid=message.sender_environment_conductor,
            )
            environment_records.append(environment_record)
            self._dbh.commit()
            self._known_environments[
                (
                    message.experiment_run_instance_id,
                    message.experiment_run_phase,
                    message.environment_id,
                )
            ] = environment_record.id
            self._environment_ticks[
                (
                    message.experiment_run_instance_id,
                    message.experiment_run_phase,
                    message.environment_id,
                )
            ] = 0
        except sqlalchemy.exc.IntegrityError as e:
            LOG.error(
                "%s encountered multiple copies of Environment(uid=%s) in the "
                "database already present for experiment_run_instance=%s and "
                "experiment_run_phase=%s. I'm not going to add another one. "
                "Expect more strange errors ahead... (%s)",
                self,
                message.environment_id,
                message.experiment_run_instance_id,
                message.experiment_run_phase,
                e,
            )
            self._dbh.rollback()

    def _get_environment_id(
        self,
        experiment_run_instance_id: str,
        experiment_run_phase: int,
        environment_id: str,
    ) -> dbm.Environment:
        """Retrieves a store record of an environment from cache or DB."""
        index_key = (
            experiment_run_instance_id,
            experiment_run_phase,
            environment_id,
        )
        if index_key not in self._known_environments:
            query = (
                sqlalchemy.select(
                    dbm.ExperimentRunInstance,
                    dbm.ExperimentRunPhase,
                    dbm.Environment,
                )
                .join(dbm.ExperimentRunInstance.experiment_run_phases)
                .join(dbm.ExperimentRunPhase.environments)
                .where(
                    dbm.ExperimentRunInstance.uid
                    == experiment_run_instance_id,
                    dbm.ExperimentRunPhase.number == experiment_run_phase,
                    dbm.Environment.uid == environment_id,
                )
            )
            result = self._dbh.execute(query).one()
            self._known_environments[index_key] = result[dbm.Environment].id
        return self._known_environments[index_key]

    def _write_world_state(self, message: proto.EnvironmentUpdateResponse):
        try:
            environment_record_id = self._get_environment_id(
                experiment_run_instance_id=message.experiment_run_instance_id,
                experiment_run_phase=message.experiment_run_phase,
                environment_id=message.sender_environment_id,
            )
        except sqlalchemy.orm.exc.MultipleResultsFound:
            LOG.error(
                "%s found multiple records for the same Environment(uid=%s) "
                "during %s. "
                "Duplicates should not occur here; expect more errors ahead.",
                self,
                repr(message),
            )
            return
        except sqlalchemy.orm.exc.NoResultFound:
            LOG.error(
                "%s found no record for the Environment(uid=%s) "
                "during %s. "
                "Was there no environment setup? Expect more errors ahead.",
                self,
                message.sender_environment_id,
                repr(message),
            )
            return

        # Add a new world state. We don't use parent.append() here, because
        # we don't want to end up with a big augmented list...

        index_key = (
            message.experiment_run_instance_id,
            message.experiment_run_phase,
            message.sender_environment_id,
        )
        if message.simtime and message.simtime.simtime_ticks:
            self._environment_ticks[index_key] = message.simtime.simtime_ticks
        else:
            self._environment_ticks[index_key] += 1
        world_state_record = dbm.WorldState(
            simtime_ticks=self._environment_ticks[index_key],
            simtime_timestamp=(
                message.simtime.simtime_timestamp if message.simtime else None
            ),
            walltime=message.walltime,
            done=message.is_terminal,
            state_dump=message.sensors,
            environment_id=environment_record_id,
        )
        self._dbh.add(world_state_record)
        self._dbh.commit()

    def _write_agent(self, message: proto.AgentSetupRequest):
        query = (
            sqlalchemy.select(
                dbm.ExperimentRunInstance, dbm.ExperimentRunPhase
            )
            .join(dbm.ExperimentRunInstance.experiment_run_phases)
            .where(
                dbm.ExperimentRunInstance.uid
                == message.experiment_run_instance_id,
                dbm.ExperimentRunPhase.number == message.experiment_run_phase,
            )
        )
        try:
            result = self._dbh.execute(query).one()
        except sqlalchemy.orm.exc.MultipleResultsFound:
            LOG.error(
                "StoreReceiver(id=0x%x, uid=%s) "
                "encountered an AgentSetupRequest("
                "experiment_run_id=%s, experiment_run_instance_id=%s, "
                "experiment_run_phase=%s), "
                "but there are duplicate entries for this run phase. "
                "I will not record this agent as I do not know to which "
                "phase it belongs. "
                "Expect more errors from the store ahead.",
                id(self),
                self.uid,
                message.experiment_run_id,
                message.experiment_run_instance_id,
                message.experiment_run_phase,
            )
            return
        except sqlalchemy.orm.exc.NoResultFound:
            LOG.error(
                "StoreReceiver(id=0x%x, uid=%s) "
                "encountered an AgentSetupRequest("
                "experiment_run_id=%s, experiment_run_instance_id=%s, "
                "experiment_run_phase=%s), "
                "but there is no record of this phase in the store. "
                "I will not record this agent as I cannot do it; "
                "expect more errors from the store ahead.",
                id(self),
                self.uid,
                message.experiment_run_id,
                message.experiment_run_instance_id,
                message.experiment_run_phase,
            )
            return

        agent_records = result[dbm.ExperimentRunPhase].agents
        try:
            agent_records.append(
                dbm.Agent(
                    uid=message.receiver_agent_conductor,
                    name=message.agent_name,
                    configuration=message.configuration,
                    muscles=[],
                )
            )
            self._dbh.commit()
        except sqlalchemy.exc.IntegrityError as e:
            LOG.error(
                "StoreReceiver(id=0x%x, uid=%s) "
                "encountered multiple copies of Agent(uid=%s) in the database "
                "already present for experiment_run_instance=%s and "
                "experiment_run_phase=%s. I'm not going to add another one. "
                "Expect more strange errors ahead... (%s)",
                id(self),
                self.uid,
                message.agent_id,
                message.experiment_run_instance_id,
                message.experiment_run_phase,
                e,
            )
            self._dbh.rollback()

    def _write_muscles(self, message: proto.AgentSetupResponse):
        query = (
            sqlalchemy.select(
                dbm.ExperimentRunInstance,
                dbm.ExperimentRunPhase,
                dbm.Agent,
            )
            .join(dbm.ExperimentRunInstance.experiment_run_phases)
            .join(dbm.ExperimentRunPhase.agents)
            .where(
                dbm.Agent.uid == message.sender_agent_conductor,
                dbm.ExperimentRunPhase.number == message.experiment_run_phase,
                dbm.ExperimentRunInstance.uid
                == message.experiment_run_instance_id,
            )
        )
        try:
            record = self._dbh.execute(query).one()
        except sqlalchemy.orm.exc.MultipleResultsFound:
            LOG.error(
                "StoreReceiver(id=0x%x, uid=%s) "
                "encountered an AgentSetupResponse("
                "agent_conductor_id=%s, agent_id=%s, "
                "experiment_run_id=%s, experiment_run_instance_id=%s, "
                "experiment_run_phase=%s), "
                "but there are duplicate entries for this run phase. "
                "I will not record this agent's muscles as I do not know to "
                "which agent it belongs. "
                "Expect more errors from the store ahead.",
                id(self),
                self.uid,
                message.sender_agent_conductor,
                message.agent_id,
                message.experiment_run_id,
                message.experiment_run_instance_id,
                message.experiment_run_phase,
            )
            return
        except sqlalchemy.orm.exc.NoResultFound:
            LOG.error(
                "%s encountered an %s, "
                "but there is no record of this agent in the store. "
                "I will not record this agent's muscles as I cannot do it; "
                "expect more errors from the store ahead.",
                self,
                repr(message),
            )
            return
        agent_record = record[dbm.Agent]
        agent_record.muscles.append(message.agent_id)
        flag_modified(agent_record, "muscles")  # Mutations are not autotracked
        self._dbh.commit()
        self._known_agents[
            (
                message.experiment_run_instance_id,
                message.experiment_run_phase,
                message.agent_id,
            )
        ] = agent_record.id

    def _get_agent_id(
        self,
        experiment_run_instance_id: str,
        experiment_run_phase: int,
        agent_id: str,
    ) -> dbm.Agent:
        index_key = (
            experiment_run_instance_id,
            experiment_run_phase,
            agent_id,
        )
        if index_key not in self._known_agents:
            query = (
                sqlalchemy.select(
                    dbm.ExperimentRunInstance,
                    dbm.ExperimentRunPhase,
                    dbm.Agent,
                )
                .join(dbm.ExperimentRunInstance.experiment_run_phases)
                .join(dbm.ExperimentRunPhase.agents)
                .where(
                    dbm.Agent.muscles.cast(Text).contains(agent_id),
                    dbm.ExperimentRunPhase.number == experiment_run_phase,
                    dbm.ExperimentRunInstance.uid
                    == experiment_run_instance_id,
                )
            )
            self._known_agents[index_key] = (
                self._dbh.execute(query).one()[dbm.Agent].id
            )
        return self._known_agents[index_key]

    def _write_agent_inputs(self, message: proto.AgentUpdateRequest):
        try:
            agent_record_id = self._get_agent_id(
                experiment_run_instance_id=message.experiment_run_instance_id,
                experiment_run_phase=message.experiment_run_phase,
                agent_id=message.receiver_agent_id,
            )
        except sqlalchemy.orm.exc.MultipleResultsFound:
            LOG.error(
                "StoreReceiver(id=0x%x, uid=%s) "
                "encountered an %s, "
                "but there are duplicate entries for this agent/run phase. "
                "This agent's inputs will be ignored and not stored, because "
                "I do not know to which agent it belongs."
                "Expect more errors from the store ahead.",
                id(self),
                self.uid,
                repr(message),
            )
            return
        except sqlalchemy.orm.exc.NoResultFound:
            LOG.error(
                "StoreReceiver(id=0x%x, uid=%s) "
                "encountered an %s, "
                "but there is no record of this agent in the store. "
                "I will not record this agent's inputs as I do not know to "
                "which agent it might belong. "
                "Expect more errors from the store ahead.",
                id(self),
                self.uid,
                repr(message),
            )
            return

        muscle_action_record = dbm.MuscleAction(
            simtimes=message.simtimes,
            walltime=message.walltime,
            sensor_readings=message.sensors,
            agent_id=agent_record_id,
        )

        # Update the last action's reward, and then finally store it:

        try:
            last_action = self._last_known_muscle_actions.pop(
                message.receiver_agent_id
            )
            last_action.rewards = message.rewards
            self._dbh.add(last_action)
            self._dbh.commit()
        except KeyError:
            pass  # Expected the first time - ask for forgiveness is pythonian.

        # Cache the current one - we still have some internal updating to do:
        # (cf. _write_agent_actions):
        self._last_known_muscle_actions[
            message.receiver_agent_id
        ] = muscle_action_record

    def _write_agent_actions(self, message: proto.AgentUpdateResponse):
        try:
            last_muscle_inputs = self._last_known_muscle_actions[
                message.sender_agent_id
            ]
        except KeyError:
            LOG.error(
                "%s could not find matching last action for %s, skipping",
                self,
                repr(message),
            )
            return

        # Just update here internally. It is saved to the DB on a later pass
        # in _write_agent_inputs when the next AgentUpdateRequest arrives:
        last_muscle_inputs.actuator_setpoints = message.actuator_information

    def _invalidate_cache(
        self, message: proto.SimulationControllerTerminationResponse
    ):
        """Cleans the local cache after a experiment run phase has ended."""
        if message.restart:
            return  # Don't clean on restarts!
        self._environment_ticks = {
            k: v
            for k, v in self._environment_ticks.items()
            if (
                k[0] != message.experiment_run_instance_id
                and k[1] != message.experiment_run_phase
            )
        }
        self._known_environments = {
            k: v
            for k, v in self._known_environments.items()
            if (
                k[0] != message.experiment_run_instance_id
                and k[1] != message.experiment_run_phase
            )
        }
        self._known_agents = {
            k: v
            for k, v in self._known_agents.items()
            if (
                k[0] != message.experiment_run_instance_id
                and k[1] != message.experiment_run_phase
            )
        }

    @staticmethod
    def _read(msg):
        """Unpacks a message, filters ignores"""

        _ = msg.pop(0)
        empty = msg.pop(0)
        assert empty == b""
        _ = msg.pop(0)
        # if len(msg) >= 1:
        #     serv_comm = msg.pop(0)
        if len(msg) > 3:
            sender = msg.pop(0)
            empty = msg.pop(0)
            header = msg.pop(0)
            LOG.debug(
                "Ignored message parts: %s, %s, %s", sender, empty, header
            )

        if msg[0] == MDP.W_HEARTBEAT:
            # We ignore heartbeats
            return "ignore", None, None
        if msg[0] == MDP.W_READY:
            return "ignore", None, None

        if len(msg) == 1:
            # it is a response
            uid = ""
            msg_obj = StoreReceiver._deserialize(msg.pop(0))
            msg_type = "response"

        elif len(msg) == 2:
            uid = StoreReceiver._deserialize(msg.pop(0))
            msg_obj = StoreReceiver._deserialize(msg.pop(0))
            msg_type = "request"
        else:
            uid = ""
            msg_obj = "None"
            msg_type = "error"

        return msg_type, uid, msg_obj

    @staticmethod
    def _deserialize(msg):
        try:
            msg = deserialize([msg])
            return msg
        except zlib.error:
            LOG.debug(
                "StoreReceiver received a message '%s', "
                "which could not be deserialized from zlib.",
                msg,
            )
        try:
            msg = str(msg.decode())
            return msg
        except AttributeError:
            LOG.debug(
                "StoreReceiver received a message '%s', "
                "which could not be str-decoded. ",
                msg,
            )
        return msg

    def __str__(self):
        return "StoreReceiver(id=0x%x, uid=%s, uri=%s)" % (
            id(self),
            self.uid,
            self._store_uri,
        )
