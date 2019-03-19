#!/usr/bin/env python

"""plot_results.py: Plot results from OBDA simulation"""

__author__ = "Murray Ireland"
__email__ = "murray@craftprospect.com"
__date__ = "22/10/2018"
__copyright__ = "Copyright 2018 Craft Prospect Ltd"

import os, cv2
import matplotlib.pyplot as plt
import numpy as np

# Get current and base directories
cur_dir = os.path.dirname(os.path.realpath(__file__))
if "\\" in cur_dir:
    base_dir = "/".join(cur_dir.split("\\"))
else:
    base_dir = cur_dir

def PlotResults(save_data, plots="all"):
    """Plot results as trajectory over Earth map and time histories"""

    # Extract time histories
    data = save_data["Data"]

    ax_range = [
        np.amin(save_data["Corners"][:, 0]),
        np.amax(save_data["Corners"][:, 0]),
        -np.amin(save_data["Corners"][:, 1]),
        -np.amax(save_data["Corners"][:, 1])
    ]

    print(save_data["Corners"])

    # Axis limits
    xlims, ylims = ax_range[:2], ax_range[2:]

    # Figure dpi
    dpi = 100

    if plots == "all" or "ground track" in plots:
        """Plot satellite ground track"""

        # Load texture
        img = cv2.imread(cur_dir + "/images/samp1_small.jpg")
        img = img[::-1, :, ::-1].transpose(1, 0, 2)

        fig, ax = plt.subplots(dpi=dpi, figsize=[12, 5], facecolor="white")
        ax.imshow(img, extent=ax_range)

        # Plot satellite trajectory
        ax.plot(data["Pos"][0, :], data["Pos"][1, :], "g")

        # Plot camera sight trajectory
        ax.plot(data["Target pos"][0, :], data["Target pos"][1, :], c="r")

        # Plot target positions
        for pos in data["Target info"]["Pos"]:
            ax.scatter(pos[0], pos[1])

    if plots == "all" or "attitude" in plots:
        """Plot satellite attitude"""

        fig, axs = plt.subplots(2, 1, dpi=dpi, facecolor="white", figsize=[7, 8])

        axs[0].plot(data["Time"], data["Att"][1, :]*180/np.pi)
        axs[0].plot(data["Time"], data["Inputs"][1, :]*180/np.pi)
        axs[0].set_ylabel("Pitch [deg]")

        axs[1].plot(data["Time"], data["Att"][2, :]*180/np.pi)
        axs[1].plot(data["Time"], data["Inputs"][2, :]*180/np.pi)
        axs[1].set_ylabel("Yaw [deg]")

        for ax in axs:
            ax.set_xlabel("Time [s]")
            ax.set_xlim(data["Time"][[0, -1]])
            ax.grid()
    
    if plots == "all" or "energy" in plots:
        """Plot satellite energy"""
        
        fig, axs = plt.subplots(1, 1, dpi=dpi, facecolor="white", figsize=[7, 4])

        axs.plot(data["Time"], data["Energy"])
        axs.set_xlabel("Time [s]")
        axs.set_ylabel("Energy [W hr]")
        axs.set_xlim(data["Time"][[0, -1]])
        axs.grid()

    plt.show()

def VisResults(save_data):
    """Visualise OBDA results using VTK"""

    from visualisation import Visualisation

    vis = Visualisation(save_data["Props"], save_data["Data"])

if __name__ == "__main__":
    """Main function"""

    save_data = np.load(f"{cur_dir}/save_data_qkd.npy").item()

    for key, value in save_data.items():
        if type(value) is dict:
            print(f"{key}:")
            for key2, value2 in value.items():
                if type(value2) is dict:
                    print(f"  {key2}:")
                    for key3, value3 in value2.items():
                        if type(value3) is np.ndarray:
                            print(f"    {key3}: {type(value3)} Size: {value3.shape}")
                        elif type(value3) is list or type(value3) is tuple:
                            print(f"    {key3}: {type(value3)} Size: {len(value3)}")
                        else:
                            print(f"    {key3}: {type(value3)}")
                elif type(value2) is np.ndarray:
                    print(f"  {key2}: {type(value2)} Size: {value2.shape}")
                elif type(value2) is list or type(value2) is tuple:
                    print(f"  {key2}: {type(value2)} Size: {len(value2)}")
                else:
                    print(f"  {key2}: {type(value2)}")
        else:
            print(f"{key}: {type(value)} Size: {value.shape}")

    # Plots
    PlotResults(save_data, "all")

    # Visualisation
    # VisResults(save_data)
