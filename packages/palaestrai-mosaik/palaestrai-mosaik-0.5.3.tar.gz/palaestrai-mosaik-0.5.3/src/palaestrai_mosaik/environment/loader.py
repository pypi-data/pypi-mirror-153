"""This module contains the function :func:`.load_funcs` to load a
mosaik environment.

This comprises to instantiate a world object und retrieve sensor and
actuator descriptions

"""
from __future__ import annotations

from importlib import import_module
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Tuple, Union

if TYPE_CHECKING:
    from mosaik import World
    from palaestrai.agent.actuator_information import ActuatorInformation
    from palaestrai.agent.sensor_information import SensorInformation


def load_funcs(
    module_name: str, description_func: str, instance_func: str
) -> Tuple[
    Callable[[Dict[str, Any]], World],
    Callable[
        [Dict[str, Any]],
        Tuple[
            List[Union[SensorInformation, Dict[str, Any]]],
            List[Union[ActuatorInformation, Dict[str, Any]]],
        ],
    ],
]:
    """Load the description functions.

    Expects a dictionary containing the keys *"module"*,
    *"description_func"*, and "instance_func". *"module"* can
    either be a python module or a python class. The path segments
    for modules are separated by a dot "." and a class is separated
    by a colon ":", e.g., if *descriptor* is a module::

        {
            "module": "midas.adapter.harlequin.descriptor",
            "description_func": "describe",
            "instance_func": "get_world",
        }

    or, if *Descriptor* is a class::

        {
            "module": "midas.adapter.harlequin:Descriptor",
            "description_func": "describe",
            "instance_func": "get_world",
        }


    Parameters
    ----------
    params : dict
        A *dict* containing the keys as described above.

    Returns
    -------
    tuple
        A *tuple* of the description function and the instance
        function.

    """

    if ":" in module_name:
        module, clazz = module_name.split(":")
        module = import_module(module)
        obj = getattr(module, clazz)()
    else:
        obj = import_module(module_name)

    dscr_func = getattr(obj, description_func)
    inst_func = getattr(obj, instance_func)

    return dscr_func, inst_func
