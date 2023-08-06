import unittest
from copy import deepcopy
from pathlib import Path
from queue import Queue
from tempfile import TemporaryDirectory
from typing import Optional
from unittest.mock import patch

import jsonpickle
import numpy as np
from sqlalchemy import select

import palaestrai.core.protocol
import palaestrai.store.database_model as dbm
from palaestrai.agent import (
    RewardInformation,
    SensorInformation,
    ActuatorInformation,
)
from palaestrai.core import RuntimeConfig
from palaestrai.experiment import ExperimentRun
from palaestrai.store.database_util import setup_database
from palaestrai.store.receiver import StoreReceiver
from palaestrai.types import Box, Mode


class TestReceiver(unittest.TestCase):
    experiment_run = ExperimentRun.load(
        Path(__file__).parent
        / ".."
        / ".."
        / ".."
        / "fixtures"
        / "dummy_run.yml"
    )

    # Store all messages that we care about in the test as a list in order to
    # replay them piece by piece:
    messages = [
        palaestrai.core.protocol.ExperimentRunStartRequest(
            sender_executor_id="executor",
            receiver_run_governor_id="run_governor",
            experiment_run_id="MockExperimentRun-0",
            experiment_run=experiment_run,
        ),
        palaestrai.core.protocol.SimulationStartRequest(
            sender_run_governor_id="RunGovernor-0",
            receiver_simulation_controller_id="SimulationController-0",
            experiment_run_id=experiment_run.uid,
            experiment_run_instance_id=experiment_run.instance_uid,
            experiment_run_phase=42,
            experiment_run_phase_id="Phase 42",
            experiment_run_phase_configuration={"mode": "TRAINING"},
        ),
        palaestrai.core.protocol.EnvironmentSetupResponse(
            sender_environment_conductor="EnvironmentConductor-0",
            receiver_simulation_controller="SimulationController-0",
            experiment_run_id=experiment_run.uid,
            experiment_run_instance_id=experiment_run.instance_uid,
            experiment_run_phase=42,
            environment_id="Environment-0",
            environment_parameters={"Mock": "Parameters", "For": "Testing"},
            environment_type="DummyEnvironment",
        ),
        palaestrai.core.protocol.EnvironmentUpdateResponse(
            sender_environment_id="Environment-0",
            receiver_simulation_controller_id="SimulationController-0",
            experiment_run_id=experiment_run.uid,
            experiment_run_instance_id=experiment_run.instance_uid,
            experiment_run_phase=42,
            sensors=[
                SensorInformation(
                    sensor_id="MockSensor-0",
                    sensor_value=08.15,
                    observation_space=Box(low=[0.0], high=[10.0]),
                )
            ],
            rewards=[
                RewardInformation(
                    reward_value=23,
                    observation_space=Box(low=[0.0], high=[47.0]),
                    reward_id="PseudoReward",
                )
            ],
            is_terminal=False,
        ),
        palaestrai.core.protocol.AgentSetupRequest(
            sender_simulation_controller="SimulationController-0",
            receiver_agent_conductor="AgentConductor-0",
            experiment_run_id=experiment_run.uid,
            experiment_run_instance_id=experiment_run.instance_uid,
            experiment_run_phase=42,
            agent_id="Agent-0",
            agent_name="Agent-0",
            configuration={"Agent": "Configuration", "Name": "Agent-0"},
            sensors=[
                SensorInformation(
                    sensor_id="MockSensor-0",
                    sensor_value=08.15,
                    observation_space=Box(low=[0.0], high=[10.0]),
                ),
                SensorInformation(
                    sensor_id="MockSensor-1",
                    sensor_value=42.47,
                    observation_space=Box(low=[0.0], high=[66.6]),
                ),
            ],
            actuators=[
                ActuatorInformation(
                    actuator_id="MockActor-47",
                    setpoint=23.0,
                    action_space=Box(low=[-47.0], high=[+47.0]),
                )
            ],
        ),
        palaestrai.core.protocol.AgentSetupResponse(
            sender_agent_conductor="AgentConductor-0",
            receiver_simulation_controller="SimulationController-0",
            experiment_run_id=experiment_run.uid,
            experiment_run_instance_id=experiment_run.instance_uid,
            experiment_run_phase=42,
            agent_id="Agent-0",
        ),
        palaestrai.core.protocol.AgentUpdateRequest(
            sender_simulation_controller_id="SimulationController-0",
            receiver_agent_id="Agent-0",
            experiment_run_id=experiment_run.uid,
            experiment_run_instance_id=experiment_run.instance_uid,
            experiment_run_phase=42,
            sensors=[
                SensorInformation(
                    sensor_id="MockSensor-0",
                    sensor_value=08.15,
                    observation_space=Box(low=[0.0], high=[10.0]),
                ),
                SensorInformation(
                    sensor_id="MockSensor-1",
                    sensor_value=42.47,
                    observation_space=Box(low=[0.0], high=[66.6]),
                ),
            ],
            actuators=[
                ActuatorInformation(
                    actuator_id="MockActor-47",
                    setpoint=23.0,
                    action_space=Box(low=[-47.0], high=[+47.0]),
                )
            ],
            is_terminal=False,
            rewards=[
                RewardInformation(
                    reward_value=23,
                    observation_space=Box(low=[0.0], high=[47.0]),
                    reward_id="PseudoReward",
                )
            ],
            mode=Mode.TRAIN,
        ),
        palaestrai.core.protocol.AgentUpdateResponse(
            sender_agent_id="Agent-0",
            receiver_simulation_controller_id="SimulationController-0",
            experiment_run_id=experiment_run.uid,
            experiment_run_instance_id=experiment_run.instance_uid,
            experiment_run_phase=42,
            sensor_information=[
                SensorInformation(
                    sensor_id="MockSensor-0",
                    sensor_value=08.15,
                    observation_space=Box(low=[0.0], high=[10.0]),
                ),
                SensorInformation(
                    sensor_id="MockSensor-1",
                    sensor_value=42.47,
                    observation_space=Box(low=[0.0], high=[66.6]),
                ),
            ],
            actuator_information=[
                ActuatorInformation(
                    actuator_id="MockActor-47",
                    setpoint=23.0,
                    action_space=Box(low=[-47.0], high=[+474747.0]),
                )
            ],
        ),
    ]

    def setUp(self) -> None:
        self.tempdir: Optional[TemporaryDirectory] = TemporaryDirectory()
        self.store_path = f"{self.tempdir.name}/palaestrai.db"
        self.store_uri = f"sqlite:///{self.store_path}"
        RuntimeConfig().reset()
        RuntimeConfig().load({"store_uri": self.store_uri})
        setup_database(self.store_uri)
        self.queue: Queue = Queue()
        self.store: Optional[StoreReceiver] = StoreReceiver(self.queue)

    def tearDown(self) -> None:
        self.store = None
        self.tempdir = None

    def test_handles_all_protocol_messages(self):
        all_message_types = [
            v
            for k, v in palaestrai.core.protocol.__dict__.items()
            if k.endswith("Request") or k.endswith("Response")
        ]
        for t in all_message_types:
            try:
                _ = self.store._message_dispatch[t]
            except KeyError:
                self.fail(
                    f"Message type {t} raises key error as it is unknown to "
                    f"the store receiver's dispatcher."
                )

    def test_stores_experiment_run(self):
        self.store.write(TestReceiver.messages[0])
        q = self.store._dbh.query(dbm.Experiment).join(dbm.ExperimentRun)
        self.assertEqual(q.count(), 1)
        experiment_record = q.first()
        self.assertEqual(len(experiment_record.experiment_runs), 1)
        experiment_run_record = experiment_record.experiment_runs[0]
        self.assertEqual(
            experiment_run_record.uid, TestReceiver.experiment_run.uid
        )
        self.assertIsInstance(experiment_run_record.document, ExperimentRun)
        experiment_run_json = jsonpickle.Unpickler().restore(
            experiment_run_record._document_json
        )
        self.assertIsNotNone(experiment_run_json)
        self.assertEqual(
            experiment_run_json.uid, TestReceiver.experiment_run.uid
        )
        q = self.store._dbh.query(dbm.ExperimentRunInstance)
        self.assertEqual(1, q.count())
        q = (
            self.store._dbh.query(dbm.Experiment)
            .join(dbm.ExperimentRun)
            .join(dbm.ExperimentRunInstance)
        )
        self.assertEqual(1, q.count())

    def test_stores_experiment_run_phase(self):
        self.store.write(TestReceiver.messages[0])
        self.store.write(TestReceiver.messages[1])
        q = self.store._dbh.query(dbm.ExperimentRunInstance)
        self.assertEqual(q.count(), 1)
        experiment_run_instance_record = q.first()
        self.assertIsNotNone(experiment_run_instance_record)
        self.assertEqual(
            experiment_run_instance_record.uid,
            TestReceiver.experiment_run.instance_uid,
        )
        q = self.store._dbh.query(dbm.ExperimentRunPhase)
        self.assertEqual(1, q.count())
        q = (
            self.store._dbh.query(dbm.Experiment)
            .join(dbm.ExperimentRun)
            .join(dbm.ExperimentRunInstance)
            .join(dbm.ExperimentRunPhase)
        )
        self.assertEqual(1, q.count())
        r = q.first()
        experiment_run_phase_record = (
            r.experiment_runs[0]
            .experiment_run_instances[0]
            .experiment_run_phases[0]
        )
        self.assertEqual(
            TestReceiver.messages[1].experiment_run_phase,
            experiment_run_phase_record.number,
        )
        self.assertEqual(
            TestReceiver.messages[1].experiment_run_phase_id,
            experiment_run_phase_record.uid,
        )
        self.assertEqual(
            TestReceiver.messages[1].experiment_run_phase_configuration,
            experiment_run_phase_record.configuration,
        )

        second_phase_start_request = deepcopy(TestReceiver.messages[1])
        second_phase_start_request.experiment_run_phase = 1
        second_phase_start_request.experiment_run_phase_id = "SecondPhase"
        second_phase_start_request.experiment_run_phase_configuration = {
            "mode": "TESTING",
            "episodes": 23,
        }
        self.store.write(second_phase_start_request)
        q = select(dbm.ExperimentRunPhase)
        r = self.store._dbh.execute(q).all()
        self.assertEqual(2, len(r))
        experiment_run_phase_record = r[1][dbm.ExperimentRunPhase]
        self.assertEqual(
            experiment_run_phase_record.configuration,
            second_phase_start_request.experiment_run_phase_configuration,
        )

    def test_stores_environment(self):
        self.store.write(TestReceiver.messages[0])
        self.store.write(TestReceiver.messages[1])
        self.store.write(TestReceiver.messages[2])
        q = self.store._dbh.query(dbm.Environment)
        self.assertEqual(1, q.count())
        q = (
            self.store._dbh.query(dbm.Experiment)
            .join(dbm.ExperimentRun)
            .join(dbm.ExperimentRunInstance)
            .join(dbm.ExperimentRunPhase)
            .join(dbm.Environment)
            .filter(
                dbm.Environment.uid == TestReceiver.messages[2].environment_id
            )
        )
        self.assertEqual(1, q.count())
        r = (
            q.first()
            .experiment_runs[0]
            .experiment_run_instances[0]
            .experiment_run_phases[0]
            .environments[0]
        )
        self.assertEqual(TestReceiver.messages[2].environment_id, r.uid)
        self.assertEqual(TestReceiver.messages[2].environment_type, r.type)
        self.assertIsNotNone(r.parameters)

    def test_stores_world_state(self):
        self.store.write(TestReceiver.messages[0])
        self.store.write(TestReceiver.messages[1])
        self.store.write(TestReceiver.messages[2])
        self.store.write(TestReceiver.messages[3])
        q = self.store._dbh.query(dbm.WorldState)
        self.assertEqual(1, q.count())

        additional_world_state = deepcopy(TestReceiver.messages[3])
        additional_world_state.is_terminal = True
        self.store.write(additional_world_state)
        q = self.store._dbh.query(dbm.WorldState).order_by(
            dbm.WorldState.simtime_ticks
        )
        self.assertEqual(2, q.count())
        self.assertEqual(1, q[0].simtime_ticks)
        self.assertEqual(2, q[1].simtime_ticks)
        self.assertTrue(additional_world_state.is_terminal, q[1].done)

        q = (
            self.store._dbh.query(dbm.Experiment)
            .join(dbm.ExperimentRun)
            .join(dbm.ExperimentRunInstance)
            .join(dbm.ExperimentRunPhase)
            .join(dbm.Environment)
            .join(dbm.WorldState)
            .filter(
                dbm.Environment.uid == TestReceiver.messages[2].environment_id
            )
        )
        self.assertEqual(2, q.count())
        world_states = (
            q.first()
            .experiment_runs[0]
            .experiment_run_instances[0]
            .experiment_run_phases[0]
            .environments[0]
            .world_states
        )
        self.assertFalse(world_states[0].done)
        self.assertTrue(world_states[1].done)

    @patch("palaestrai.store.receiver.LOG")
    def test_stores_agent(self, logmock):
        self.store.write(TestReceiver.messages[0])
        self.store.write(TestReceiver.messages[1])
        self.store.write(TestReceiver.messages[4])
        self.assertFalse(logmock.critical.called)

        q = self.store._dbh.query(dbm.Agent)
        self.assertEqual(1, q.count())

        additional_run_phase = deepcopy(TestReceiver.messages[1])
        additional_run_phase.experiment_run_phase = 47
        additional_run_phase.experiment_run_phase_id = "Phase 47"
        self.store.write(additional_run_phase)
        q = self.store._dbh.query(dbm.ExperimentRunPhase)
        self.assertEqual(2, q.count())
        q = self.store._dbh.query(dbm.Agent)
        self.assertEqual(1, q.count())

        additional_agent_setup_request = deepcopy(TestReceiver.messages[4])
        additional_agent_setup_request.experiment_run_phase = (
            additional_run_phase.experiment_run_phase
        )
        self.store.write(additional_agent_setup_request)
        self.assertFalse(logmock.critical.called)
        q = self.store._dbh.query(dbm.ExperimentRunPhase)
        self.assertEqual(2, q.count())
        q = self.store._dbh.query(dbm.Agent)
        self.assertEqual(2, q.count())
        q = (
            select(dbm.ExperimentRunInstance, dbm.ExperimentRunPhase)
            .join(dbm.ExperimentRunInstance.experiment_run_phases)
            .where(
                dbm.ExperimentRunInstance.uid
                == additional_run_phase.experiment_run_instance_id,
                dbm.ExperimentRunPhase.number
                == additional_run_phase.experiment_run_phase,
            )
        )
        r = self.store._dbh.execute(q).all()
        self.assertEqual(1, len(r))
        self.assertEqual(1, len(r[0][dbm.ExperimentRunPhase].agents))

    @patch("palaestrai.store.receiver.LOG")
    def test_stores_muscles(self, logmock):
        self.store.write(TestReceiver.messages[0])
        self.store.write(TestReceiver.messages[1])
        self.store.write(TestReceiver.messages[4])
        self.store.write(TestReceiver.messages[5])
        self.assertFalse(logmock.critical.called)

        q = select(dbm.Agent).where(
            dbm.Agent.uid == TestReceiver.messages[5].sender_agent_conductor
        )
        r = self.store._dbh.execute(q).all()
        self.assertEqual(
            [TestReceiver.messages[5].agent_id], r[0][dbm.Agent].muscles
        )

    @patch("palaestrai.store.receiver.LOG")
    def test_stores_muscle_inputs(self, logmock):
        self.store.write(TestReceiver.messages[0])
        self.store.write(TestReceiver.messages[1])
        self.store.write(TestReceiver.messages[4])
        self.store.write(TestReceiver.messages[5])
        self.store.write(TestReceiver.messages[6])
        self.assertFalse(
            logmock.critical.called, msg=logmock.critical.call_args
        )
        self.assertFalse(logmock.error.called, msg=logmock.critical.call_args)
        self.assertFalse(
            logmock.warning.called, msg=logmock.critical.call_args
        )

        self.assertEqual(
            len(self.store._last_known_muscle_actions.values()), 1
        )

        self.store.write(TestReceiver.messages[7])
        self.store.write(TestReceiver.messages[6])
        r = self.store._dbh.execute(select(dbm.Agent)).all()
        self.assertEqual(1, len(r[0][dbm.Agent].muscle_actions))
        r = self.store._dbh.execute(select(dbm.MuscleAction)).all()
        self.assertEqual(1, len(r))
        self.assertIsNotNone(r[0][dbm.MuscleAction].rewards)

        self.store.write(TestReceiver.messages[7])
        self.store.write(TestReceiver.messages[6])
        r = self.store._dbh.execute(select(dbm.Agent)).all()
        self.assertEqual(len(r[0][dbm.Agent].muscle_actions), 2)
        r = self.store._dbh.execute(select(dbm.MuscleAction)).all()
        self.assertEqual(len(r), 2)
        self.assertIsNotNone(r[0][dbm.MuscleAction].rewards)

    @patch("palaestrai.store.receiver.LOG")
    def test_stores_muscle_actions(self, logmock):
        self.store.write(TestReceiver.messages[0])
        self.store.write(TestReceiver.messages[1])
        self.store.write(TestReceiver.messages[4])
        self.store.write(TestReceiver.messages[5])
        self.store.write(TestReceiver.messages[6])
        self.store.write(TestReceiver.messages[7])
        self.store.write(TestReceiver.messages[6])
        self.assertFalse(
            logmock.critical.called, msg=logmock.critical.call_args
        )
        self.assertFalse(logmock.error.called, msg=logmock.critical.call_args)
        self.assertFalse(
            logmock.warning.called, msg=logmock.critical.call_args
        )

        r = self.store._dbh.execute(
            select(dbm.MuscleAction).order_by(dbm.MuscleAction.id)
        ).all()
        self.assertIsNotNone(r[0][dbm.MuscleAction].actuator_setpoints)

        self.store.write(TestReceiver.messages[7])
        self.store.write(TestReceiver.messages[6])
        self.assertFalse(
            logmock.critical.called, msg=logmock.critical.call_args
        )
        r = self.store._dbh.execute(
            select(dbm.MuscleAction).order_by(dbm.MuscleAction.id)
        ).all()
        self.assertIsNotNone(r[0][dbm.MuscleAction].actuator_setpoints)

        r = self.store._dbh.execute(
            select(dbm.MuscleAction).order_by(dbm.MuscleAction.id)
        ).all()
        self.assertIsNotNone(r[0][dbm.MuscleAction].actuator_setpoints)
        self.assertIsNotNone(r[1][dbm.MuscleAction].actuator_setpoints)

    @patch("palaestrai.store.receiver.LOG")
    def test_stores_world_states_with_infinity(self, logmock):
        self.store.write(TestReceiver.messages[0])
        self.store.write(TestReceiver.messages[1])
        self.store.write(TestReceiver.messages[2])

        environment_update_response = deepcopy(TestReceiver.messages[3])
        environment_update_response.sensors = [
            SensorInformation(
                sensor_id="MockSensor-0",
                sensor_value=np.Infinity,
                observation_space=Box(low=[0.0], high=[10.0]),
            ),
            SensorInformation(
                sensor_id="MockSensor-1",
                sensor_value=np.NaN,
                observation_space=Box(low=[0.0], high=[10.0]),
            ),
        ]
        try:
            self.store.write(environment_update_response)
        except Exception as e:
            self.fail(str(e))
        self.assertFalse(
            logmock.critical.called, msg=logmock.critical.call_args
        )
        r = self.store._dbh.execute(select(dbm.WorldState)).one()
        self.assertTrue(
            all(s()[0] is None for s in r[dbm.WorldState].state_dump),
            msg="NaN and Infinity must be converted to NULL/None",
        )

    def test_stores_rewards(self):
        # Setup agent:
        self.store.write(TestReceiver.messages[0])
        self.store.write(TestReceiver.messages[1])

        # Agent setup requests, write the agent (conductors):
        agent_setup_request_1 = deepcopy(TestReceiver.messages[4])
        agent_setup_request_1.receiver_agent_conductor = "AC-0"
        agent_setup_request_1.agent_name = "AC-0"
        self.store.write(agent_setup_request_1)
        agent_setup_request_2 = deepcopy(TestReceiver.messages[4])
        agent_setup_request_2.receiver_agent_conductor = "AC-1"
        agent_setup_request_2.agent_name = "AC-1"
        self.store.write(agent_setup_request_2)

        # Agent setup responses: Write muscles:
        agent_setup_response_1 = deepcopy(TestReceiver.messages[5])
        agent_setup_response_1.sender_agent_conductor = "AC-0"
        agent_setup_response_1.agent_id = "A"
        agent_setup_response_2 = deepcopy(TestReceiver.messages[5])
        agent_setup_response_2.sender_agent_conductor = "AC-1"
        agent_setup_response_2.agent_id = "B"
        self.store.write(agent_setup_response_2)
        self.store.write(agent_setup_response_1)

        # Now write some fake actions:

        N_ACTIONS = 32
        for i in range(N_ACTIONS):
            agent_update_request_1 = deepcopy(TestReceiver.messages[6])
            agent_update_request_1.receiver_agent_id = "A"
            agent_update_request_1.rewards[0].reward_value = float(i)
            agent_update_response_1 = deepcopy(TestReceiver.messages[7])
            agent_update_response_1.sender_agent_id = "A"
            agent_update_response_1.actuator_information[0].setpoint = [
                float(i)
            ]
            agent_update_request_2 = deepcopy(TestReceiver.messages[6])
            agent_update_request_2.receiver_agent_id = "B"
            agent_update_request_2.rewards[0].reward_value = float(2 * i)
            agent_update_response_2 = deepcopy(TestReceiver.messages[7])
            agent_update_response_2.sender_agent_id = "B"
            agent_update_response_2.actuator_information[0].setpoint = [
                float(2 * i)
            ]
            self.store.write(agent_update_request_1)
            self.store.write(agent_update_request_2)
            self.store.write(agent_update_response_2)
            self.store.write(agent_update_response_1)

        # Check for data:

        result = self.store._dbh.execute(
            select(dbm.MuscleAction).where(dbm.MuscleAction.agent_id == "A")
        ).all()
        for i, ma in enumerate(result):
            if i < N_ACTIONS - 1:  # Last action has no reward
                self.assertEqual(
                    float(i + 1), ma[dbm.MuscleAction].rewards[0].reward_value
                )
            self.assertEqual(
                float(i), ma[dbm.MuscleAction].actuator_setpoints[0].setpoint
            )

        result = self.store._dbh.execute(
            select(dbm.MuscleAction).where(dbm.MuscleAction.agent_id == "B")
        ).all()
        for i, ma in enumerate(result):
            if i < N_ACTIONS - 1:  # Last action has no reward
                self.assertEqual(
                    float(2 * (i + 1)),
                    ma[dbm.MuscleAction].rewards[0].reward_value,
                )
            self.assertEqual(
                float(2 * i),
                ma[dbm.MuscleAction].actuator_setpoints[0].setpoint,
            )


if __name__ == "__main__":
    unittest.main()
