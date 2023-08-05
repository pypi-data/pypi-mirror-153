"""This module contains exceptions."""


class ShutdownError(Exception):
    """This error is raised to kill mosaik on purpose.

    Mosaik will not see the error raising and simply crash (in the same
    way mosaik is killed with a keyboard interrupt).

    No responsibility is taken for any damage on unfinished simulators
    waiting for their next step.

    Such a sadness!

    """
