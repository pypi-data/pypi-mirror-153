"""This module contains the debug script that can be used to start
the dummy experiment without the CLI.

"""
import asyncio
import logging
import os
import sys

from palaestrai.cli.manager import init_logger
from palaestrai.core import RuntimeConfig
from palaestrai.experiment.executor import Executor, ExecutorState, Experiment


def main(filename="dummy_experiment", verbose=0, use_custom_logging=False):
    # runtime_file = os.path.abspath(
    #     os.path.join(
    #         __file__, "..", "..", "fixtures", "arl-runtime-debug.conf.yaml"
    #     )
    # )
    # with open(runtime_file) as f:
    #     conf = f.read()

    RuntimeConfig().load()

    init_logger(verbose)
    if use_custom_logging:
        custom_logging()

    # experiment_file = os.path.abspath(
    #     os.path.join(__file__, "..", "..", "fixtures", f"{filename}.yml")
    # )
    try:
        experiment = Experiment.load(filename)
    except (NotADirectoryError, FileNotFoundError):
        experiment_file = os.path.abspath(
            os.path.join(__file__, "..", "..", "fixtures", f"{filename}.yml")
        )
        experiment = Experiment.load(experiment_file)
        print(
            "Ignore that stupid, annoying error message. "
            "I already found the file!!1."
        )

    executor = Executor()
    executor.schedule(experiment)
    executor_final_state = asyncio.run(executor.execute())
    if executor_final_state != ExecutorState.EXITED:
        sys.exit(
            {
                ExecutorState.SIGINT: -2,
                ExecutorState.SIGABRT: -6,
                ExecutorState.SIGTERM: -15,
            }[executor_final_state]
        )


def custom_logging():
    """Manually configure palaestrai loggers."""
    logging.getLogger("palaestrai").setLevel("ERROR")
    logging.getLogger("palaestrai.agent").setLevel("ERROR")
    logging.getLogger("palaestrai.core").setLevel("ERROR")
    logging.getLogger("palaestrai.store").setLevel("ERROR")
    logging.getLogger("palaestrai.experiment").setLevel("ERROR")
    logging.getLogger("palaestrai.environment").setLevel("ERROR")
    logging.getLogger("palaestrai.util").setLevel("ERROR")
    logging.getLogger("palaestrai_mosaik").setLevel("DEBUG")
    logging.getLogger("palaestrai_mosaik.environment").setLevel("ERROR")
    logging.getLogger("palaestrai_mosaik.mosaikpatch").setLevel("ERROR")
    logging.getLogger("palaestrai_mosaik.simulator").setLevel("ERROR")

    logging.getLogger("pandapower").setLevel("ERROR")
    logging.getLogger("matplotlib").setLevel("ERROR")
    logging.getLogger("h5py").setLevel("ERROR")
    logging.getLogger("midas").setLevel("DEBUG")
    logging.getLogger("pysimmods").setLevel("ERROR")
    logging.getLogger("numexpr").setLevel("ERROR")


if __name__ == "__main__":
    # main("dummy_experiment", use_custom_logging=True)
    main("example_experiment_midas", use_custom_logging=True)
