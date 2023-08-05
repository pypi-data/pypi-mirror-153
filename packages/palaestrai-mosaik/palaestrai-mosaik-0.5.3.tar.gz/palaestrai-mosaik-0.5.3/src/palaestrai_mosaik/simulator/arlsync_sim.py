"""This module contains the :class:`.ARLSyncSimulator`, which is used
by the :class:`.MosaikEnvironment` for synchronization.

"""
import mosaik_api
from palaestrai_mosaik.config import AGENT_EID
from palaestrai_mosaik.simulator import LOG

META = {
    "type": "time-based",
    "models": {
        AGENT_EID: {
            "public": True,
            "any_inputs": True,
            "params": ["env"],
            "attrs": [],
        }
    },
}


class ARLSyncSimulator(mosaik_api.Simulator):
    """A simulator for the synchronization of palaestrAI and mosaik.

    Attributes
    ----------
    sid : str
        The simulator id for this simulator given by mosaik
    step_size : int
        The step_size of this simulator
    models : dict
        A dictionary containing all models of this simulator.
        Currently, there is no reason why there should be more than one
        agent model.

    """

    def __init__(self):
        super().__init__(META)
        self.sid = None
        self.step_size = None
        self.models = dict()

        self._env = None

    def init(self, sid, **sim_params):
        """Initialize this simulator.

        Called exactly ones after the simulator has been started.

        Parameters
        ----------
        sid : str
            Simulator id provided by mosaik.

        Returns
        -------
        dict
            The meta description for this simulator as *dict*.

        """
        self.sid = sid
        self._env = sim_params["env"]
        self.step_size = sim_params["step_size"]

        return self.meta

    def create(self, num, model, **model_params):
        """Initialize the simulation model instance (entity)

        Parameters
        ----------
        num : int
            The number of models to create in one go.
        model : str
            The model to create. Needs to be present in the META.

        Returns
        -------
        list
            A *list* of the entities created during this call.

        """
        assert model == AGENT_EID

        entities = list()

        for _ in range(num):
            eid = f"{AGENT_EID}-{len(self.models)}"
            self.models[eid] = {
                "model": model,
                "eid": eid,
            }
            entities.append({"eid": eid, "type": model})
        return entities

    def step(self, time, inputs, max_advance=0):
        """Perform a simulation step.

        Parameters
        ----------
        time : int
            The current simulation time (the current step).
        inputs : dict
            A *dict* with inputs for the models.

        Returns
        -------
        int
            The simulation time at which this simulator should
            perform its next step.

        """

        LOG.debug("Stepped ARLSyncSim at step %d", time)

        self._env.sync(time)

        return time + self.step_size

    def get_data(self, outputs):
        """Return requested outputs (if feasible).

        Since this simulator does not generate output for its own, an
        empty dict is returned.

        Parameters
        ----------
        outputs : dict
            Requested outputs.

        Returns
        -------
        dict
            An empty dictionary, since no output is generated.

        """
        return dict()
