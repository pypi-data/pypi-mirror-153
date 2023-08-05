Example: MIDAS 
==============

Have a look in the source code under tests/example_experiment_midas.yml.
The configuration is not final, yet, but this example file should work
if you have installed everything (midas, pysimmods, palaestrai, and
palaestrai-mosaik).

Run the example
---------------

To run the midas example, just pass the experiment file to the 
palaestrai CLI:

.. code-block:: bash

    $ palaestraictl experiment-start tests/fixtures/example_experiment_midas.yml

Changing Sensors and Actuators
------------------------------

Each agent is defined in the example_experiment_midas.yml file and has
a field for sensors and actuators. You can change them to your liking.
A list of all sensors and actuators in the environment are listed below
the regular definition.
