# CommonRoad Agent Simulation

This repository comprises module to perform multi agent simulations with [CommonRoad](https://commonroad.in.tum.de) scenarios.
Dynamic obstacles in a scenario can be replaced by agents with certain behavior models implemented in this repository.
This allows to perfom simulations with interacting traffic participants that do not follow predefined trajectories but react on other traffic participants.

Supported Behavior Models
==========================
If nothing specified the dynamic obstacles in a scenario move according to the predefined trajectories.
If assigned like shown in the [examples](/examples/), the scenario can be simulated forward with the ``step()`` while the considered dynamic obstacles behave according to the specified behavior model.
Currently, the following behavior models are implemented:

**IDM**

The IDM is a well known car following model. It does not include lane changes and is suited best for highway scenarios. An example can be found [here](/examples/idm_example.py)

**MOBIL**

MOBIL is an extension of the IDM with lane change decisions. An example can be found [here](/examples/mobil_example.py)

**LEVEL_0_POLICY**

The level 0 policy defines a basic behavior of an interaction unaware traffic participant. This policy will be used to train higher level agents with reasoning hierarchy.


Installation
=============
The following need to be installed on your machine:

**Requirements**

* Python >= 3.6

Installation via pip:

`pip install commonroad-agent`