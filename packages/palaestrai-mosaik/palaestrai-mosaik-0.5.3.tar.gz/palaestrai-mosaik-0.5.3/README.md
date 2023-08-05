# Adversarial Resilience Learning --- Mosaik Environment

This projects contains the interface between palaestrAI and mosaik, 
the mosaik environment.

## Introduction

This package allows to use worlds created with the co-simulation 
framework mosaik as environment in palaestrAI. The package was 
developed with MIDAS in mind but should work for arbitrary mosaik
worlds. See documenation for more details on how to import a world.

## Installation

palaestrAI-mosaik is written in Python. It provides a `setup.py` that installs
the minimal set of packages to run ARL Mosaik. Use, preferable in a
virtual environment::

     ./setup.py install

or, for development::

    pip install -e .

Additional requirements are listed in the requirements.txt::

    pip install -r requirements.txt

Alternatively, you can install it directly with pip

    pip install palaestrai-mosaik


## Usage

To run an example you have to install the requirements.txt. 
Under tests, you find the `example_experiment_midas.yml` that should be
passed to the palaestrai command line interface::

    palaestrai experiment-start /path/to/tests/example_experiment_midas.yml
