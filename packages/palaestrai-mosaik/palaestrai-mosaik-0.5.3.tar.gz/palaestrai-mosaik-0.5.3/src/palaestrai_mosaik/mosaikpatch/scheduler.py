"""This module contains a modified version of the mosaik scheduler.

Since the scheduler is not a class but a collection of functions,
each function of the scheduler needs to be present. For most of them,
calls can be directed to the regular scheduler function. However, as
soon as the mosaik scheduler changes, these changes need to be
reflected here and new functions need a forward call in this module.

The only function with a modification is the
:func:`mosaik.scheduler.get_input_data` function (and there is added
only one line of code). But to make use of this modified function, it
is required to provide copies of :func:`mosaik.scheduler.run` and
:func:`mosaik.scheduler.sim_process`, as well. They should be updated
on a new mosaik version.

See
https://mosaik.readthedocs.io/en/latest/api_reference/mosaik.scheduler.html
for the docs of the original functions.

Tested with mosaik version 2.6.0

"""
from time import perf_counter

import mosaik.scheduler
import pkg_resources

# Get major mosaik version
MM_VERSION = int(pkg_resources.require("mosaik")[0].version.split(".")[0])
if MM_VERSION >= 3:
    from mosaik.exceptions import (
        NoStepException,
        SimulationError,
        WakeUpException,
    )

from palaestrai_mosaik.mosaikpatch import LOG
from simpy.exceptions import Interrupt


def run(
    world,
    until,
    rt_factor=None,
    rt_strict=False,
    print_progress=True,
    lazy_stepping=True,
):
    """Run the simulation.

    This is an exact copy of the current :func:`mosaik.scheduler.run`
    method.

    """

    if MM_VERSION < 3:
        print(
            "It seems you're not using the latest Mosaik version. "
            "Please consider updating:\n\n\tpip install --upgrade mosaik\n"
        )
    world.until = until
    if rt_factor is not None and rt_factor <= 0:
        raise ValueError('"rt_factor" is %s but must be > 0"' % rt_factor)
    if rt_factor is not None:
        # Adjust rt_factor to the time_resolution:
        rt_factor *= world.time_resolution
    world.rt_factor = rt_factor

    env = world.env

    setup_done_events = []
    for sim in world.sims.values():
        if sim.meta["api_version"] >= (2, 2):
            # setup_done() was added in API version 2.2:
            setup_done_events.append(sim.proxy.setup_done())

    yield env.all_of(setup_done_events)

    processes = []
    for sim in world.sims.values():
        if MM_VERSION >= 3:
            process = env.process(
                sim_process3(
                    world,
                    sim,
                    until,
                    rt_factor,
                    rt_strict,
                    print_progress,
                    lazy_stepping,
                )
            )
        else:
            process = env.process(
                sim_process2(
                    world, sim, until, rt_factor, rt_strict, print_progress
                )
            )

        sim.sim_proc = process
        processes.append(process)

    yield env.all_of(processes)


def sim_process2(world, sim, until, rt_factor, rt_strict, print_progress):
    """SimPy simulation process for a certain simulator *sim*.

    This method is an exact copy of the current
    :func:`mosaik.scheduler.sim_process` method.

    """

    rt_start = perf_counter()

    try:
        keep_running = get_keep_running_func(world, sim, until)
        while keep_running():
            try:
                yield step_required(world, sim)
            except StopIteration:
                # We've been woken up by a terminating successor.
                # Check if we can also stop or need to keep running.
                continue

            yield wait_for_dependencies(world, sim)
            input_data = get_input_data(world, sim)
            yield from rt_sleep(rt_factor, rt_start, sim, world)
            yield from step(world, sim, input_data)
            rt_check(rt_factor, rt_start, rt_strict, sim)
            yield from get_outputs(world, sim)
            world.sim_progress = get_progress(world.sims, until)
            if print_progress:
                print("Progress: %.2f%%" % world.sim_progress, end="\r")

        # Before we stop, we wake up all dependencies who may be waiting for
        # us. They can then decide whether to also stop of if there's another
        # process left for which they need to provide data.
        for pre_sid in world.df_graph.predecessors(sim.sid):
            evt = world.sims[pre_sid].step_required
            if not evt.triggered:
                evt.fail(StopIteration())

    except ConnectionError as err:
        raise SimulationError(
            f"Simulator '{sim.sid}' closed its connection.", err
        )


def sim_process3(
    world, sim, until, rt_factor, rt_strict, print_progress, lazy_stepping
):
    """
    SimPy simulation process for a certain simulator *sim*.
    """
    sim.rt_start = rt_start = perf_counter()

    try:
        keep_running = get_keep_running_func(
            world, sim, until, rt_factor, rt_start
        )
        while keep_running():
            try:
                yield from has_next_step(world, sim)
            except WakeUpException:
                # We've been woken up by a terminating predecessor.
                # Check if we can also stop or need to keep running.
                continue
            except NoStepException:
                # None of the simulators has a next step, therefore stop.
                break
            sim.interruptable = True
            while True:
                try:
                    yield from rt_sleep(rt_factor, rt_start, sim, world)
                    yield wait_for_dependencies(world, sim, lazy_stepping)
                    break
                except Interrupt as i:
                    assert i.cause == "Earlier step"
                    clear_wait_events(sim)
                    continue
            sim.interruptable = False
            input_data = get_input_data(world, sim)
            max_advance = get_max_advance(world, sim, until)
            yield from step(world, sim, input_data, max_advance)
            rt_check(rt_factor, rt_start, rt_strict, sim)
            yield from get_outputs(world, sim)
            notify_dependencies(world, sim)
            if world._df_cache:
                prune_dataflow_cache(world)
            world.sim_progress = get_progress(world.sims, until)
            if print_progress:
                print("Progress: %.2f%%" % world.sim_progress, end="\r")
        sim.progress_tmp = until
        sim.progress = until
        clear_wait_events_dependencies(sim)
        check_and_resolve_deadlocks(sim, end=True)
        # Before we stop, we wake up all dependencies who may be waiting for
        # us. They can then decide whether to also stop of if there's another
        # process left which might provide data.
        for suc_sid in world.trigger_graph.successors(sim.sid):
            if not world.sims[suc_sid].sim_proc.triggered:
                evt = world.sims[suc_sid].has_next_step
                if not evt.triggered:
                    world.sims[suc_sid].sim_proc.interrupt("Stopped simulator")

    except ConnectionError as e:
        raise SimulationError(
            'Simulator "%s" closed its connection.' % sim.sid, e
        )


def get_input_data(world, sim):
    """Return a dictionary with the input data for *sim*.

    The original function :func:`mosaik.scheduler.get_input_data` is
    called. Afterwards, the :func:`~.trigger_actuators` method of the
    modified world object is called.

    """
    input_data = mosaik.scheduler.get_input_data(world, sim)

    LOG.debug("Now triggering actuators for sim %s", sim.sid)

    # This is the modification for ARL
    world.trigger_actuators(sim, input_data)
    # This was the modification for ARL

    return input_data


def get_next_step(sim):
    return mosaik.scheduler.get_next_step(sim)


def has_next_step(world, sim):
    return mosaik.scheduler.has_next_step(world, sim)


def get_max_advance(world, sim, until):
    return mosaik.scheduler.get_max_advance(world, sim, until)


def treat_cycling_output(world, sim, data, output_time):
    return mosaik.scheduler.treat_cycling_output(world, sim, data, output_time)


def notify_dependencies(world, sim):
    return mosaik.scheduler.notify_dependencies(world, sim)


def prune_dataflow_cache(world):
    return mosaik.scheduler.prune_dataflow_cache(world)


def check_and_resolve_deadlocks(sim, waiting=False, end=False):
    return mosaik.scheduler.check_and_resolve_deadlocks(sim, waiting, end)


def clear_wait_events(sim):
    return mosaik.scheduler.clear_wait_events(sim)


def clear_wait_events_dependencies(sim):
    return mosaik.scheduler.clear_wait_events_dependencies(sim)


def step(world, sim, inputs, max_advance=0):
    """Step the scheduler.

    See :func:`mosaik.scheduler.step`.

    """
    if MM_VERSION >= 3:
        return mosaik.scheduler.step(world, sim, inputs, max_advance)
    else:
        return mosaik.scheduler.step(world, sim, inputs)


def get_outputs(world, sim):
    """Get outputs for a simulator.

    See :func:`mosaik.scheduler.get_outputs`.

    """
    return mosaik.scheduler.get_outputs(world, sim)


def get_progress(sims, until):
    """Get simulation progress.

    See :func:`mosaik.scheduler.get_progress`.

    """
    return mosaik.scheduler.get_progress(sims, until)


def rt_sleep(rt_factor, rt_start, sim, world):
    """Sleep for real time simulation.

    See :func:`mosaik.scheduler.rt_sleep`.

    """
    return mosaik.scheduler.rt_sleep(rt_factor, rt_start, sim, world)


def rt_check(rt_factor, rt_start, rt_strict, sim):
    """Check the time for real time simulation.

    See :func:`mosaik.scheduler.rt_check`.

    """
    return mosaik.scheduler.rt_check(rt_factor, rt_start, rt_strict, sim)


def get_keep_running_func(world, sim, until, rt_factor=1.0, rt_start=0):
    """Return the *keep_running_func*.

    See :func:`mosaik.scheduler.get_keep_running_func`.

    """
    if MM_VERSION >= 3:
        return mosaik.scheduler.get_keep_running_func(
            world, sim, until, rt_factor, rt_start
        )
    else:
        return mosaik.scheduler.get_keep_running_func(world, sim, until)


def step_required(world, sim):
    """Return if another step is required.

    See :func:`mosaik.scheduler.step_required`.

    """
    return mosaik.scheduler.step_required(world, sim)


def wait_for_dependencies(world, sim, lazy_stepping=True):
    """Wait for dependencies of *sim*.

    See :func:`mosaik.scheduler.wait_for_dependencies`.

    """
    if MM_VERSION >= 3:

        return mosaik.scheduler.wait_for_dependencies(
            world, sim, lazy_stepping
        )
    else:
        return mosaik.scheduler.wait_for_dependencies(world, sim)
