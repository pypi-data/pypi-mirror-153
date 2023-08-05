"""This module contains the :class:`.MosaikInterfaceComponent`, which
cares for all the precious sensors and actuators.

"""
from __future__ import annotations

import json
from copy import copy
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

import numpy as np
from palaestrai.agent.actuator_information import ActuatorInformation
from palaestrai.agent.sensor_information import SensorInformation
from palaestrai.types import Space
from palaestrai.util.exception import OutOfActionSpaceError
from palaestrai_mosaik.config import AGENT_FULL_ID
from palaestrai_mosaik.environment import LOG

if TYPE_CHECKING:
    from mosaik import World


class MosaikInterfaceComponent:
    """The mosaik interface component stores all sensors and actuators.

    Parameters
    ----------

    sensors : list
        List of sensor descriptions. A sensor description should either
        be an instance of
        :class:`palaestrai.agent.sensor_information.SensorInformation`
        or a dict like::

            sensor = {
                # Unique identifier of the sensor containing the
                # Simulator ID, the Entity ID, and the attribute name
                "sensor_id": <sid.eid.attr>,
                # String description of an *palaestrai.types* object
                "observation_space": "Box(low=0.0, high=1.2, "
                                     "shape=(1,), dtype=np.float32)",
            }

    actuators : list
        List of actuator descriptions. An actuator description should
        either be an instance of
        :class:`palaestrai.agent.actuator_information.ActuatorInformation`
        or a dict like::

            actuator = {
                # Unique identifier of the actuator containing the
                # Simulator ID, the Entity ID, and the attribute name
                "actuator_id": <sid.eid.attr>,
                # String description of an *palaestrai.types* object
                "action_space": "Box(low=0.0, high=1.2, "
                                "shape=(1,), dtype=np.float32)",
            }

    seed : int, optional
        A seed for the random number generator (rng). When more than
        one agent provides values for the same actuator, one of the
        values is randomly chosen.

    Attributes
    ----------
    sensors : list
        A *list* containing all :class:`~.SensorInformation` objects.
    actuators : list
        A *list* containing all :class:`~.ActuatorInformation` objects.
    sensor_map : dict
        A *dict* that stores the index of each sensor as value.
    actuator_map: dict
        A *dict* that stores the valid actuator ids as keys and the
        initial configuration of each actuator as value.

    """

    def __init__(
        self,
        sensors: List[Union[SensorInformation, Dict[str, Any]]],
        actuators: List[Union[ActuatorInformation, Dict[str, Any]]],
        seed: Optional[int] = None,
    ):
        self._sensor_defs: List[
            Union[SensorInformation, Dict[str, Any]]
        ] = sensors
        self._actuator_defs: List[
            Union[ActuatorInformation, Dict[str, Any]]
        ] = actuators

        self.sensors: List[SensorInformation] = []
        self.actuators: List[ActuatorInformation] = []
        self.sensor_map: dict = {}
        self.actuator_map: dict = {}

        self._rng: np.random.RandomState = np.random.RandomState(seed)

    def create_sensors(self) -> List[SensorInformation]:
        """Create sensors from the sensor description.

        The description is provided during initialization.

        Returns
        -------
        list
            The *list* containing the created sensor objects.

        """
        sensors = []
        for idx, sensor in enumerate(self._sensor_defs):
            if isinstance(sensor, SensorInformation):
                sensors.append(sensor)
                uid = sensor.sensor_id
            else:
                uid = str(sensor["sensor_id"])
                sensors.append(
                    SensorInformation(
                        sensor_id=uid,
                        observation_space=Space.from_string(
                            sensor["observation_space"]
                        ),
                        sensor_value=sensor.get("sensor_value", 0),
                    )
                )
            self.sensor_map[uid] = copy(sensors[-1])
        self.sensors = sensors
        return self.sensors

    def create_actuators(self) -> List[ActuatorInformation]:
        """Create actuators from the actuator description.

        The description is provided during initialization.

        Returns
        -------
        list
            The *list* containing the created actuator objects.

        """
        actuators = []
        for idx, actuator in enumerate(self._actuator_defs):
            if isinstance(actuator, ActuatorInformation):
                actuators.append(actuator)
                uid = actuator.actuator_id
            else:
                uid = str(actuator["actuator_id"])

                actuators.append(
                    ActuatorInformation(
                        setpoint=actuator.get("setpoint", None),
                        actuator_id=uid,
                        action_space=Space.from_string(
                            actuator["action_space"]
                        ),
                    )
                )

            self.actuator_map[uid] = copy(actuators[-1])

        self.actuators = actuators
        return self.actuators

    def trigger_sensors(self, world: World, time: int):
        """Fill the sensors with fresh data from mosaik.

        This method is called from within the mosaik process.
        At each sync point (i.e., the :class:`.ARLSyncSimulator` is
        stepping), all current outputs of the simulators are written
        into the sensors.

        Parameters
        ----------
        world : :class:`mosaik.scenario.World`
            The current world object.
        time : int
            The current simulation time

        """
        self.sensors = list()
        for sid, entities in getattr(world, "_df_cache")[time].items():
            for eid, attrs in entities.items():
                for attr, val in attrs.items():
                    key = f"{sid}.{eid}.{attr}"

                    if key not in self.sensor_map:
                        continue

                    LOG.debug("Trying to access sensor %s.", key)
                    try:
                        sensor = copy(self.sensor_map[key])
                    except IndexError:
                        LOG.warning(
                            "Sensor with id %s not found in available "
                            "sensors. Skipping this one.",
                            key,
                        )
                        continue
                    try:
                        val = check_value(val)
                    except TypeError:
                        LOG.warning(
                            "The type of value %s (%s) from sensor %s "
                            "could not be mapped to one of (int, float"
                            ", str, bool). Setting this value to None!",
                            val,
                            type(val),
                            key,
                        )
                        val = None
                    log_val = (
                        "{ ... }"
                        if (
                            val is not None
                            and isinstance(val, str)
                            and len(val) > 100
                        )
                        else val
                    )

                    LOG.info("Reading value %s from sensor %s.", log_val, key)
                    sensor.sensor_value = val
                    self.sensors.append(sensor)

    def get_sensor_readings(self):
        """Get all current sensor readings.

        This method is called from within the communication process.

        Returns
        -------
        list
            The *list* with all sensors and updated values.

        """
        return self.sensors

    def update_actuators(self, actuators: list):
        """Update the actuator values.

        This method is called from within the communication process.
        Removes all previous actuators from the list and adds all
        actuators from *actuators* to the list if they are present in
        the :attr:`actuator_map`.

        Parameters
        ----------
        actuators : list
            A *list* of :class:`.ActuatorInformation` objects.

        """
        self.actuators = []

        for idx, actuator in enumerate(actuators):
            assert isinstance(actuator, ActuatorInformation), (
                "provided actuator is not an instance of "
                f"{ActuatorInformation.__class__}."
            )

            if actuator.actuator_id not in self.actuator_map:
                LOG.warning(
                    "Encountered unknown actuator %s. Skipping.",
                    actuator.actuator_id,
                )
                continue

            # We won't allow dicts as actuator values
            # Every other clean up will be performed when the actuators
            # are accessed

            # try:

            #     val = actuator.setpoint
            #     if isinstance(val, dict):
            #         val = json.dumps(val)

            # except TypeError:
            #     LOG.warning(
            #         "The type of value %s (%s) from actuator %s could "
            #         " not be mapped to one of (int, float, str"
            #         ", bool). Setting this value to None!",
            #         val,
            #         type(val),
            #         actuator.actuator_id,
            #     )
            #     val = None
            # try:
            #     actuator.setpoint = val
            # except OutOfActionSpaceError:
            #     actuator.setpoint = [val]
            self.actuators.append(actuator)

    def trigger_actuators(self, sim, input_data):
        """Forward the actuator values to the specific simulators.

        This method is called from within the mosaik process.
        In contrast to the sensor calls, the actuators can only be
        triggered per simulator. Each simulator calls the mosaik
        scheduler to fetch its *input_data*. After the normal fetching
        process, the input_data dict is filled with inputs for the
        simulator *sim*.

        In this method, all actuators are checked wether they have
        "better" data or the specific input of the simulator. These
        values are updated and the old values will be overwritten. Then
        the actuators are resetted, i.e., setpoints are set to None.

        The *input_data* is then returned to the scheduler, which
        passes them to the calling simulator.

        Notes
        -----
            It is possible that some simulators may rely on multiple
            inputs for a certain attribute and throw an error after the
            ARL injection, or filter for specific data provider and,
            therefore, ignore the ARL input. As soon as this case
            occurs, this method should be adapted accordingly.

        Parameters
        ----------
        sim : :class:`mosaik.scenario.ModelMock`
            The *ModelMock* of the simulator calling the
            :func:`.get_input_data` function of the mosaik scheduler.
        input_data : dict
            The currently gathered input data for this simulator.
            ARL tries to manipulate them.

        """

        for actuator in self.actuators:
            key = actuator.actuator_id
            act_sid, act_eid, attr = key.split(".")
            if sim.sid != act_sid:
                continue
            LOG.debug("Trying to access actuator %s.", key)

            try:
                setpoint = restore_value(actuator.setpoint)
            except TypeError:
                LOG.warning(
                    "Could not restore value %s (%s) of actuator %s. "
                    "Skipping!",
                    actuator.setpoint,
                    type(actuator.setpoint),
                    key,
                )
                continue

            if setpoint is None:
                LOG.debug(
                    "The setpoint of actuator %s is None. Skipping!", key
                )
                continue

            LOG.debug(
                "Trigger actuator for %s with value %s",
                key,
                setpoint,
            )

            if attr not in input_data.setdefault(act_eid, dict()):
                input_data[act_eid][attr] = dict()
                LOG.info(
                    "Attribute %s not found in the input_data of this "
                    "simulator. Creating this entry may be cause of "
                    "some strange and unexpected behavior ...",
                    attr,
                )

            LOG.info("Setting value %s to actuator %s.", setpoint, key)
            if AGENT_FULL_ID in input_data[act_eid][attr]:
                input_data[act_eid][attr][AGENT_FULL_ID].append(setpoint)
            else:
                input_data[act_eid][attr] = {AGENT_FULL_ID: [setpoint]}

        for model, attrs in input_data.items():
            for attr, src_ids in attrs.items():
                if AGENT_FULL_ID not in src_ids:
                    continue
                assert len(src_ids) == 1
                if len(src_ids[AGENT_FULL_ID]) > 1:
                    LOG.debug(
                        "It seems more than one agent already tried to"
                        " manipulate this entry: found values %s. "
                        "May fate decide the outcome of this battle "
                        "...",
                        src_ids[AGENT_FULL_ID],
                    )
                    setpoint = self._rng.choice(src_ids[AGENT_FULL_ID])
                else:
                    setpoint = src_ids[AGENT_FULL_ID][0]
                src_ids[AGENT_FULL_ID] = setpoint


def check_value(val):

    if isinstance(val, dict):
        # A dict! Let's dump it to json
        return str(json.dumps(val))
    if isinstance(val, np.ndarray):
        # We got a numpy array! This may be root of evil, unseen
        # errors. We convert it to a list if it has multiple values,
        # otherwise we unpack it.
        LOG.warning(
            "Got numpy array %s as value. It will be converted to a "
            "list or unpacked, depending on its length.",
            val,
        )
        if len(val) > 1:
            val = list(val)
        else:
            val = val[0]
    return val


def restore_value(val):
    if isinstance(val, str):
        try:
            return json.loads(val)
        except ValueError:
            # Just a normal string
            pass

    if isinstance(val, np.ndarray):
        if len(val) > 1:
            val = list(val)
        else:
            val = val[0]
    return val
