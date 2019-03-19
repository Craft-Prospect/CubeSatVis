# Craft Prospect Visualisation

Example visualisation showing satellite with limited orbital motion.

## Overview

This repository contains the visualisation code currently used by Craft Prospect to animate and understand the results of in-house simulations. The simulation used to generate the provided results does not describe orbital motion in full (i.e. as a body circling the Earth) but as a body moving in a straight line over a flat plane. Results from a full orbital motion simulation will be provided in future.

## Files & Folders

### Scripts

| File | Description |
| - | - |
| ``plot_results.py`` | Plot time histories and trajectories from saved data or start visualisation |
| ``visualisation.py`` | Visualise saved data as a 3D animation |

### Data Files

| File | Description |
| - | - |
| ``saved_data_qkd.npy`` | Sample of saved data, from a simulation of a satellite changing attitude to transmit quantum keys to different receivers on the ground. Several visible laser emitters are mounted on the bottom of the CubeSat and are pointed by re-orienting the CubeSat in orbit. The lasers are pointed towards specific targets on the ground and pointed on/off depending on what payload mode is active. |

### Folders

| Folder | Description |
| - | - |
| ``fonts`` | Fonts used in visualisation |
| ``images`` | Earth imagery used in plots and visualisation |

## Saved Data Description

The file ``save_data_qkd.npy`` contains fixed properties which were used in the simulation and which are used to determine the geometry of the CubeSat model, Earth map, target positions, etc. It also contains arrays of time-stamped data from the simulation which is used to animate the 3D models in the visualisation. A description of the saved properties follows.

| Variable | Description |
| - | - |
| ``Data`` | A mix of time-stamped arrays describing a number of variable values at specific times and some constants produced by the simulation |
| ``Corners`` | A NumPy array describing the (x, y) positions of the four corners of the Earth texture in km from the point under satellite starting position |
| ``Props`` | Fixed settings which are defined prior to and used in both the simulation and visualisation. Some are exclusive to one or the other and may not be relevant to the visualisation. |

### ``Data`` Dictionary

#### Arrays

Each data array is produced by the simulation by sampling the given variable at specific times and appending them to the save array. For example, position is three-dimensional (x, y, z) and so at each time t is described by a list of length 3. If the simulation samples each variable 1876 times, the final position array will be (3 x 1876), describing the 3D position at each sampled time.

| Variable | Description | Dimensions | Units |
| - | - | - | - |
| ``Time`` | The time at each sample, eg. ``[0.00, 0.04, 0.08, ..., 75.00]`` | 1 | seconds |
| ``Pos `` | The position, where (0, 0, 0) is the starting point on the Earth below the satellite | 3 (x, y, z) | metre |
| ``Vel`` | The velocity in each 3D direction | 3 (xdot, ydot, zdot) | metre/sec |
| ``Att`` | The attitude (or orientation) around each 3D axis | 3 (roll, pitch, yaw) | radian |
| ``AngVel`` | The angular velocity around each 3D axis | 3 (roll vel, pitch vel, yaw vel) | radian/sec |
| ``Inputs`` | The attitude commands around each 3D axis, i.e. the satellite should rotate so that the attitude matches these values. | 3 (roll, pitch, yaw) | radian |
| ``Target pos`` | The point on the ground which any of the shown beams are intersecting, i.e. the target. | 3 (x, y, z) | metre |
| ``ADCS mode`` | The number describing the current mode of the guidance system, where the modes have names given in ``ADCS mode names``. | 1 | - |
| ``Payload mode`` | The number describing the current mode of the payload, where the modes have names given in ``Payload mode names``. The payload mode affects what beams are active within the simulation. | 1 | - |
| ``Payload temp`` | The temperature of the payload. | 1 | deg C |
| ``Energy`` | The energy level of the satellite. | 1 | Joules |

#### Fixed Properties

These variables are produced by the simulation as it runs but otherwise do not change with time.

| Property | Description | Units |
| - | - | - |
| ``Time step`` | The change in time between simulation step. | sec |
| ``Target info`` | Dictionary describing the position and visibility of each target receiver. | - |
| ``ADCS mode names`` | The names of each guidance system mode, where the index of the tuple is used to relate the name to the modes described by the ``ADCS mode`` array. | - |
| ``Payload mode names`` | The names of each payload mode, where the index of the tuple is used to relate the name to the modes described by the ``Payload mode`` array. | - |

### ``Props`` Dictionary

| Key | Description |
| - | - |
| ``Sat`` | Satellite properties, such as mass, geometry, altitude. |
| ``Camera`` | Properties of one or more onboard cameras, such as position on sat body, resolution, pitch angle, field of view. Each camera has its own dictionary. |
| ``Earth`` | Earth properties, such as mass, radius and the resolution (m/px) of the full-size texture image. |
| ``Universal`` | Universal properties describing the laws of physics |
| ``Imagery`` | Info on textures used in simulation and visualisation |
| ``Laser`` | Positions of each laser emitter on the satellite body |



