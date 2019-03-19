#!/usr/bin/env python

"""fake_orbital_data.py: Fake orbital path for visualisation and add to existing data"""

__author__ = "Murray Ireland"
__email__ = "murray@craftprospect.com"
__date__ = "22/10/2018"
__copyright__ = "Copyright 2018 Craft Prospect Ltd"

import os
import numpy as np
from numpy import sin, cos, tan, sqrt, pi

cur_dir = os.path.dirname(os.path.realpath(__file__))

# Import existing data
save_data = np.load(f"{cur_dir}/save_data_qkd.npy").item()
time_hists = save_data["Data"]
earth_props = save_data["Props"]["Earth"]
uni_props = save_data["Props"]["Universal"]

# Select orbit properties
alt = 400.e3
cubesat_mass = 5

# Orbital elements
el = {
    "sma": save_data["Props"]["Earth"]["Mean radius"] + alt, # # semi-major axis [m]
    "ecc": 0., # eccentricity [-]
    "inc": 30.*pi/180, # inclination [rad]
    "rasc": 15.*pi/180,  # right ascension of ascending node [rad]
    "argper": 0.*pi/180  # argument of perigee [rad]
}

# Gravitation parameter
mu = uni_props["Grav const"]*(earth_props["Mass"] + cubesat_mass)

# Mean angular motion
n = sqrt(mu/el["sma"]**3)

# Orbital period
T = 2*pi*sqrt(el["sma"]**3/mu)
print(f"Orbital period: {T // 60} min, {T - (T // 60)*60:.0f} secs")

# Calculate initial position and velocity in intermediate frame
EA = 0
rQ = [
    el["sma"]*cos(EA - el["ecc"]),
    el["sma"]*sqrt(1 - el["ecc"]**2)*sin(EA),
    0
]
vQ0 = [
    -sin(EA),
    sqrt(1 - el["ecc"]**2)*cos(EA),
    0
]
vQ = np.array(vQ0)*n*el["sma"]/(1 - el["ecc"]*cos(EA))

# Transform intermediate frame to ECI
R1 = np.matrix([
    [cos(el["rasc"]), -sin(el["rasc"]), 0.],
    [sin(el["rasc"]), cos(el["rasc"]), 0.],
    [0., 0., 1.]
])
R2 = np.matrix([
    [1., 0., 0.],
    [0., cos(el["inc"]), -sin(el["inc"])],
    [0., sin(el["inc"]), cos(el["inc"])]
])
R3 = np.matrix([
    [cos(el["argper"]), -sin(el["argper"]), 0.],
    [sin(el["argper"]), cos(el["argper"]), 0.],
    [0., 0., 1.]
])
R = R1*R2*R3

init_pos = (R*np.matrix(rQ).T).T.tolist()[0]
init_vel = (R*np.matrix(vQ).T).T.tolist()[0]

pos = np.array(init_pos)
vel = np.array(init_vel)

# Simulate over orbit
dt = 0.5
time_hists["Time"] = np.arange(0, np.ceil(T), dt)
time_hists["Pos"] = np.zeros((3, time_hists["Time"].shape[0]))
time_hists["Vel"] = np.zeros((3, time_hists["Time"].shape[0]))
for ind, t in enumerate(time_hists["Time"]):
    # Save data
    time_hists["Pos"][:, ind] = pos
    time_hists["Vel"][:, ind] = vel

    # States
    X = np.concatenate((pos, vel), axis=0)

    # Absolute distance
    dist = sqrt(pos[0]**2 + pos[1]**2 + pos[2]**2)

    # Acceleration
    acc = -mu/dist**3 * np.array(pos)

    # Integrate
    Xdot = np.concatenate((vel, acc), axis=0)
    X = X + dt*Xdot

    # Update variables for next loop
    pos = X[:3]
    vel = X[3:]

# Save results
np.save(os.path.join("data", "save_data_orbital.npy"), save_data)

# Plot orbit
import matplotlib.pyplot as plt

fig, axs = plt.subplots(1, 3, figsize=(18, 8))
axs[0].plot(time_hists["Pos"][0, :], time_hists["Pos"][1, :])
axs[0].set_xlabel("x [m]"), axs[1].set_ylabel("y [m]")
axs[0].set_title("View from north")
axs[1].plot(time_hists["Pos"][0, :], time_hists["Pos"][2, :])
axs[1].set_xlabel("x [m]"), axs[1].set_ylabel("z [m]")
axs[1].set_title("View from side")
axs[2].plot(time_hists["Pos"][1, :], time_hists["Pos"][2, :])
axs[2].set_xlabel("y [m]"), axs[1].set_ylabel("z [m]")
axs[2].set_title("View from side")

for ax in axs:
    ax.grid()
    ax.set_aspect("equal")

plt.show()
