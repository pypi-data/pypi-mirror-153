Getting Started
===============

This guide describes how to use *palaestrAI-mosaik* to import a mosaik 
world object into ARL. The target audience for this guide is assumed
to have at least little experience with mosaik but is new to palaestrAI.
If you don't have experience with mosaik but you just want an
environment to play with, have a look at the 
:doc:`Midas Example <midas_example>`.

Prerequisites
-------------

It is assumed that you have already followed the instructions of the
:doc:`Installation <installation>` guide.

Preparing your world
--------------------

Probably you have written mosaik scenario script that looks somehow
similar to the following example:

.. code-block:: python

    import mosaik
    SIM_CONFIG = {
        "MySimA": {
            "python": "path.to.simulatorA:Class",
        },
        "MySimB": {
            "python": "path.to.simulatorB:Class",
        },
    }
    # Define number of simulation steps
    END = 10

    # Create the world
    WORLD = mosaik.World(SIM_CONFIG)

    # Start simulators
    simA = WORLD.start("MySimA")
    simB = WORLD.start("MySimB")

    # Instantiate models
    modA = simA.ModelA()
    modB = simB.ModelB()

    # Connect entities (attrA of modA to attrB of modB)
    WORLD.connect(modA, modB, ("attrA", "attrB"))

    # Start simulation
    WORLD.run(until=END)

All you have to do is to wrap your scenario script in two functions.

Description function
--------------------

The first one should provide information about sensors and actuators
in your mosaik scenario. 

A sensor can be any attribute of a model that
is an input for another model. In the example above, this would be
*attrA* from *modA*. An actuator, on the other hand, can be any 
attribute, that is an input to a model, e.g., *attrB* of *modB*.


These sensors and actuators need to be wrapped into separate lists.
For the example above, this could look like:

.. code-block:: python

    sensor_list = [
        {
            "sensor_id": "MySimA-0.ModelA-0.attrA",
            "observation_space": "Box(low=0.0, high=1.2, "
                                 "shape=(1,), dtype=np.float32)",
        },
    ]
    actuator_list = [
        {
            "actuator_id": "MySimB-0.ModelB-0.attrB",
            "action_space": "Box(low=0.0, high=1.2, "
                            "shape=(1,), dtype=np.float32)",
        },
    ]

Here, *MySimA-0* is the simulator ID assigned from mosaik to 
simulator A, *ModelA-0* is the entity ID defined in the create method
of simulator A, and *attrA* is the name of an attribute of model A. 

The description function should return these two lists, so your new
code should look similar to this example:

.. code-block:: python

    def my_description_fnc(params=None):

        # Some code to create the lists
        # ...

        return sensor_list, actuator_list 

The argument *params* is an optional dictionary that you can use to
pass arguments to your description function. We will talk about this
in :ref:`configuration`. 

Alternatively, you can populate lists of sensor and actuator objects
provided by :class:`.SensorInformation` and 
:class:`.ActuatorInformation`, respectively:

.. code-block:: python

    from palaestrAI.agent.actuator_information import ActuatorInformation
    from palaestrAI.agent.sensor_information import SensorInformation
    from palaestrAI.types import Box

    def my_description_fnc(params=None):
        sensor_list = list()
        actuator_list = list()

        # Some other code
        # ...

        sensor_list.append(SensorInformation(
            sensor_id="MySimA-0.ModelA-0.attrA",
            observation_space: Box(
                low=0.0, high=1.2, shape=(1,), dtype=np.float32
            )
        )
        actuator_list.append(ActuatorInformation(
            actuator_id="MySimB-0.ModelB-0.attrB",
            action_space: Box(
                low=0.0, high=1.2, shape=(1,), dtype=np.float32
            )
        )
        return sensor_list, actuator_list

Instance function
-----------------

The second function that is required is the instance function, which
should return the world object created in your scenario script. 
You only have to make sure that the world has *not yet started*.
The world will be started from within *palaestrAI-mosaik*. 
The easiest way to achieve this is to wrap your scenario script in
a function. For the example script, the function could look like this:

.. code-block:: python

    import mosaik

    def my_instance_fnc(params=None):
        sim_config = {
            "MySimA": {
                "python": "path.to.simulatorA:Class",
            },
            "MySimB": {
                "python": "path.to.simulatorB:Class",
            },
        }
        # Define number of simulation steps
        end = params["end"]

        # Create the world
        world = mosaik.World(sim_config)

        # Start simulators
        simA = world.start("MySimA")
        simB = world.start("MySimB")

        # Instantiate models
        modA = simA.ModelA()
        modB = simB.ModelB()

        # Connect entities (attrA of modA to attrB of modB)
        world.connect(modA, modB, ("attrA", "attrB"))

        return world

Again, a dictionary *params* will be passed to the function. In fact,
this is the same dict that is passed to the description function. It is
up to you, in which of these functions you use the *params*. But, as 
you probably have noticed, the number of steps is fetched from the 
dict. 

That is because *palaestrAI-mosaik* needs to know, how long the
simulation should run. To make sure the correct value is passed, you
should provide the value for *end* in the params, as described in
:ref:`configuration`

Add your script to PYTHONPATH
-----------------------------

*palaestrAI-mosaik* will try to import your script and call the 
functions defined before. This will probably fail unless you add your
script to the python path. There are several ways to achieve this.

The quick-and-dirty way is to add your script (and all simulators
defined in your simulation config) to your PYTHONPATH. At the top of 
your script, add the following:

.. code-block:: python
    
    import os
    import sys
    sys.path.insert(0, os.path.abspath(__file__))


.. _configuration:

Configure the experiment file 
-----------------------------

Coming soon.


