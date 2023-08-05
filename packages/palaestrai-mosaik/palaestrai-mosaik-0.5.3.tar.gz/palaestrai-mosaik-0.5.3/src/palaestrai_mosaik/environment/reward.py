from abc import ABC
from typing import List

from palaestrai.agent import RewardInformation, SensorInformation


class Reward(ABC):
    """Abstract base class for environment rewards.

    The :class:`Reward` ABC is one way to implement a new environment
    reward. The reward is calculated from the environment view and
    measure the environment performance only. The agents use this
    reward to calculate their own internal reward by using the
    objective.

    To use the reward, it has to be called with a list of
    :class:`SensorInformation` objects::

        reward = MyReward()
        value = reward([SensorInformation(...), SensorInformation(...)])

    Parameters
    ----------
    params: dict
        A dict that can be used to pass configuration parameters to
        the reward instance.

    """

    def __init__(self, **kwargs):
        self.params: dict = kwargs

    def __call__(
        self, state: List[SensorInformation], *args, **kwargs
    ) -> List[RewardInformation]:
        raise NotImplementedError
