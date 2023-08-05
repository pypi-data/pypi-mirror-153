"""This module contains the :class:`MosaikEnvironment`, which
allows to run mosaik co-simulations with palaestrAI.

"""
from __future__ import annotations

import threading
from typing import TYPE_CHECKING, Any, Dict, Optional, Union

from palaestrai.environment.environment import Environment
from palaestrai.environment.environment_baseline import EnvironmentBaseline
from palaestrai.environment.environment_state import EnvironmentState
from palaestrai.types import SimTime
from palaestrai.util.dynaloader import load_with_params

from . import LOG
from .environment.mosaik_world import MosaikWorld
from .environment.reward import Reward
from .simulator import ShutdownError

# if TYPE_CHECKING:


class MosaikEnvironment(Environment):
    """The mosaik environment for palaestrAI.

    This class implements the abstract class
    :class:`palaestrai.environment.Environment` and allows the
    interaction between ARL agents and a mosaik co-simulation.

    Parameters
    ----------
    connection: str
        The connection to the broker, required by the *Environment*
        class.
    uid: str
        The uid of this environment, required by the *Environment*
        class.
    seed: int
        A random seed provided by the experiment.
    module: str
        Full import path to a module or class that provides the two
        functions *description_func* and *instance_func*.
    description_func: str
        Name of a function of *module* that returns information objects
        of sensors and actuators.
    instance_func: str
        Name of a function of *module* that returns a mosaik world
        object that has not yet started.
    step_size: int
        Step size in seconds for the ARL synchronization simulator.
    params: Dict[str, Any], optional
        Additional params that will be passed to *description_func* and

    Attributes
    ----------
    mworld: :class:`.MosaikWorld`
        Creates and holds the mosaik world object.

    """

    def __init__(
        self,
        uid: str,
        broker_uri: str,
        seed: int,
        module: str,
        description_func: str,
        instance_func: str,
        step_size: int,
        end: Union[int, str],
        reward: Dict[str, Any],
        params: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(uid, broker_uri, seed)

        self._module_name: str = module
        self._description_func: str = description_func
        self._instance_func: str = instance_func
        self._step_size: int = step_size
        self._end: Union[str, int] = end
        self._mosaik_params: Dict[str, Any] = {} if params is None else params

        self.mworld: MosaikWorld
        self._env_task: threading.Thread
        self._event_communicated: threading.Event
        self._event_stepped: threading.Event
        self._event_shutdown: threading.Event

        self._ctr_com: int = -1
        self._ctr_mos: int = -1
        self._shutdown: bool = False
        self._mosaik_finished: bool = False

        self.reward: Reward = load_with_params(
            reward["name"], reward["params"]
        )

    def start_environment(self):
        self._event_communicated = threading.Event()
        self._event_stepped = threading.Event()
        self._event_shutdown = threading.Event()

        self._ctr_com = -1
        self._ctr_mos = -1
        self._shutdown = False
        self._mosaik_finished = False

        LOG.debug(
            "EnvironmentCOM %s(id=0x%x, uid=%s) is creating world object "
            "...",
            self.__class__,
            id(self),
            self.uid,
        )
        self.mworld = MosaikWorld(self)
        LOG.debug(
            "EnvironmentCOM %s(id=0x%x, uid=%s) is setting up simulators, "
            "connecting entities ...",
            self.__class__,
            id(self),
            self.uid,
        )
        self.mworld.setup(
            self._module_name,
            self._description_func,
            self._instance_func,
            self._end,
            self._step_size,
            self._mosaik_params,
        )
        LOG.debug(
            "EnvironmentCOM %s(id=0x%x, uid=%s) is starting mosaik "
            "simulation process ... ",
            self.__class__,
            id(self),
            self.uid,
        )
        self._env_task = threading.Thread(target=self.start)
        self._env_task.start()
        LOG.info(
            "EnvironmentCOM %s(id=0x%x, uid=%s) finished setup. "
            "Co-simulation is now running.",
            self.__class__,
            id(self),
            self.uid,
        )
        return EnvironmentBaseline(
            sensors_available=self.mifs.sensors,
            actuators_available=self.mifs.actuators,
            simtime=SimTime(
                simtime_ticks=0, simtime_timestamp=self.mworld.now_dt
            ),
        )

    def update(self, actuators):
        """Update the environment with new actuator values.

        On each call,  *actuators* contains new values, which will be
        injected into the mosaik data graph so that simulators can
        fetch these values without even noticing.

        This method implements the communication part of the
        synchronization between worker process and the mosaik process.

        Parameters
        ----------
        actuators : list[ActuatorInformation]
            A *list* of actuators with new values provided by the
            agents.

        Returns
        -------
        tuple
            A *tuple* containing a *list*, a *float*, and a *bool*
            The list contains sensors with updated values, the float
            represents a reward defining the current state of the
            environment, and the bool is False if the environment is
            still running and True otherwise.

        """
        LOG.debug(
            "EnvironmentCOM %s(id=0x%x, uid=%s) New update request.",
            self.__class__,
            id(self),
            self.uid,
        )

        if len(actuators) > 0:
            LOG.debug(
                "EnvironmentCOM %s(id=0x%x, uid=%s) Now updating "
                "actuators ...",
                self.__class__,
                id(self),
                self.uid,
            )
            self.mifs.update_actuators(actuators)
        else:
            LOG.debug(
                "EnvironmentCOM %s(id=0x%x, uid=%s) actuator list "
                "is empty!",
                self.__class__,
                id(self),
                self.uid,
            )

        self._ctr_com += 1
        if self._mosaik_finished:
            LOG.debug(
                "EnvironmentCOM %s(id=0x%x, uid=%s) noticed that "
                "mosaik finished.",
                self.__class__,
                id(self),
                self.uid,
            )
            sensors = self.mifs.get_sensor_readings()
            reward = self.reward(sensors)
            return EnvironmentState(
                sensor_information=sensors,
                rewards=reward,
                done=True,
                simtime=SimTime(
                    simtime_ticks=self.mworld.simtime,
                    simtime_timestamp=self.mworld.now_dt,
                ),
            )

        while self._ctr_mos <= self._ctr_com:
            if self._mosaik_finished:
                LOG.debug(
                    "EnvironmentCOM %s(id=0x%x, uid=%s) noticed that "
                    "mosaik finished.",
                    self.__class__,
                    id(self),
                    self.uid,
                )
                sensors = self.mifs.get_sensor_readings()
                reward = self.reward(sensors)
                return EnvironmentState(
                    sensor_information=sensors,
                    rewards=reward,
                    done=True,
                    simtime=SimTime(
                        simtime_ticks=self.mworld.simtime,
                        simtime_timestamp=self.mworld.now_dt,
                    ),
                )
            self._event_communicated.set()
            self._event_stepped.wait()
            self._event_stepped.clear()

        LOG.debug(
            "EnvironmentCOM %s(id=0x%x, uid=%s): Now mosaik should be "
            "waiting. Starting communication ...",
            self.__class__,
            id(self),
            self.uid,
        )
        sensors = self.mifs.get_sensor_readings()
        reward = self.reward(sensors)
        LOG.debug(
            "EnvironmentCOM %s(id=0x%x, uid=%s) received sensor "
            "readings %s from mosaik at time %d (%s)",
            self.__class__,
            id(self),
            self.uid,
            sensors,
            self.mworld.simtime,
            self.mworld.now_dt,
        )

        return EnvironmentState(
            sensor_information=sensors,
            rewards=reward,
            done=False,
            simtime=SimTime(
                simtime_ticks=self.mworld.simtime,
                simtime_timestamp=self.mworld.now_dt,
            ),
        )

    def sync(self, time):
        """Allow synchronization with the message worker.

        This method is called each time the :class:`.ARLSyncSimulator`
        steps. Updates the values in the sensor objects directly from
        the mosaik data graph.

        The actuator values will not be set here, since each simulator
        fetches its input data directly and independently from mosaik.

        This method implements the mosaik part of the synchronization
        between worker and mosaik process.

        Parameters
        ----------
        time : int
            The current simulation time (current step) is required to
            retrieve the correct data from the mosaik world.

        """
        LOG.debug(
            "EnvironmentMOS %s(id=0x%x, uid=%s) updated.",
            self.__class__,
            id(self),
            self.uid,
        )
        self.mworld.update_sim_time(time)
        self.mifs.trigger_sensors(self.mworld.world, time)

        self._ctr_mos += 1

        if self._shutdown:
            raise ShutdownError
        LOG.debug(
            "EnvironmentMOS %s(id=0x%x, uid=%s) signalling COM ...",
            self.__class__,
            id(self),
            self.uid,
        )
        while self._ctr_mos > self._ctr_com:
            self._event_stepped.set()
            if self._shutdown:
                raise ShutdownError
            self._event_communicated.wait()
            self._event_communicated.clear()

        LOG.debug(
            "EnvironmentMOS %s(id=0x%x, uid=%s): now com should be "
            "waiting. Start next step ...",
            self.__class__,
            id(self),
            self.uid,
        )

    def shutdown(self, reset=False):
        """Try to shutdown the environment.

        Returns
        -------
        bool
            True if the environment was shut down, False otherwise.

        """
        LOG.info(
            "EnvironmentCOM %s(id=0x%x, uid=%s) attempting to stop "
            "the co-simulation ...",
            self.__class__,
            id(self),
            self.uid,
        )
        self._shutdown = True
        self._event_communicated.set()

        self._env_task.join()

        self._event_shutdown.wait()
        LOG.debug(
            "EnvironmentCOM %s(id=0x%x, uid=%s) The counter for mosaik "
            "should be -1 if the shutdown was "
            "sucessful. Counter value is : %d",
            self.__class__,
            id(self),
            self.uid,
            self._ctr_mos,
        )
        self.is_terminal = not reset
        return self._mosaik_finished

    def start(self):
        """Start the simulation process.

        As soon as the mosaik simulation is finished (or interrupted),
        events are set to notify the worker that the simulation is
        finished.

        """
        self.mworld.start()
        self._ctr_mos = -1
        self._mosaik_finished = True
        self._event_shutdown.set()
        self._event_stepped.set()

    @property
    def mifs(self):
        """Return the mosaik interface component.

        Holds the sensors and actuators and handles the exchange of
        data between the communication worker and the mosaik simpy
        process.

        Returns
        -------
        :class:`.MosaikInterfaceComponent`

        """
        return self.mworld.mifs
