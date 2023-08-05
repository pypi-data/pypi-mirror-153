Installation
============

This guide describes how to install *palaestrAI-mosaik* on :ref:`linux`.
OS-X and Windows are, sadly, not supported by *palaestrAI* 
(see :ref:`osx-windows`).

It is assumed that the *palaestrAI* package is already installed. In future 
versions it will be possible that we add *palaestrAI* as install 
dependency, but for now it is required to install that package 
manually. 

.. _linux:

Linux
-----

This guide is based on *Manjaro 20.2.1 Nibia, 64bit*, but this should
for work for other distributions as well.

The *palaestrAI-mosaik* package requires `Python`__ >= 3.8. We 
recommend to use a `virtualenv`__ to avoid messing up your system
environment. Use your distributions' package manager to install pip
and virtualenv.

.. code-block:: bash

    $ virtualenv ~/.virtualenvs/arl 
    $ source ~/.virtualenv/arl/bin/activate

If your distribution still relies on Python 2.x, make sure that you
actually create a virtualenv environment for Python 3.

.. code-block:: bash

    $ virtualenv -p /usr/bin/python3 ~/.virtualenvs/arl
    $ source ~/.virtualenv/arl/bin/activate

Now you can install *palaestrAI-mosaik* from the source code. 

.. code-block:: bash

    (arl) $ pip install git+https://gitlab.com/arl2/palaestrai-mosaik.git

Or, if you've provided an ssh key in your account settings:

.. code-block:: bash

    (arl) $ pip install git+ssh://git@gitlab.com:arl2/palaestrai-mosaik.git



__ https://www.python.org/
__ https://virtualenv.readthedocs.org

.. _osx-windows:

OS-X and Windows
----------------

Sadly, Windows and OS-X are not supported. The reason for this are, first,
the multiprocessing policy of *palaestrAI* that is uses *fork*, which is 
not supported by Windows and OS-X and, secondly, the signal handling for
graceful termination uses some operations that are available to UNIX only.
See the *palaestrAI* main repository for updates on these issues. 

For now windows user, we recommend to use the Windows Subsystem for Linux
and follow the instructions for :ref:`linux`.
