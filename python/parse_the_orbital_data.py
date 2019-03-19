import numpy as np
import pandas as pd
import os

data = np.load(os.path.join("data", 'save_data_orbital.npy'))
print (data)
data_dict = data.item()["Data"]
corners_list = data.item()["Corners"]
props_dict = data.item()["Props"]

time_step = data_dict["Time step"]; del data_dict["Time step"]
target_info = data_dict["Target info"]; del data_dict["Target info"]
adcs_mode = data_dict["ADCS mode names"]; del data_dict["ADCS mode names"]
payload_mode = data_dict["Payload mode names"]; del data_dict["Payload mode names"]

fixed_df = pd.DataFrame()
fixed_df['time_step'] = pd.Series(time_step)
fixed_df['adcs_mode'] = pd.Series(adcs_mode[0])
fixed_df['payload_mode'] = pd.Series(payload_mode[0])
fixed_df['target_info'] = pd.Series(target_info)

new_df = pd.DataFrame.from_dict(target_info)
corners_df = pd.DataFrame()
corners_df["bottom_left"] = pd.Series(corners_list[0])
corners_df["bottom_right"] = pd.Series(corners_list[1])
corners_df["top_right"] = pd.Series(corners_list[2])
corners_df["top_left"] = pd.Series(corners_list[3])

df = pd.DataFrame()
df['time'] = pd.Series(data_dict["Time"])

df['xpos'] = pd.Series(data_dict["Pos"][0])
df['ypos'] = pd.Series(data_dict["Pos"][1])
df['zpos'] = pd.Series(data_dict["Pos"][2])

df['xdot'] = pd.Series(data_dict["Vel"][0])
df['ydot'] = pd.Series(data_dict["Vel"][1])
df['zdot'] = pd.Series(data_dict["Vel"][2])

df['roll'] = pd.Series(data_dict["Att"][0])
df['pitch'] = pd.Series(data_dict["Att"][1])
df['yaw'] = pd.Series(data_dict["Att"][2])

df['ang_roll'] = pd.Series(data_dict["AngVel"][0])
df['ang_pitch'] = pd.Series(data_dict["AngVel"][1])
df['ang_yaw'] = pd.Series(data_dict["AngVel"][2])

df['in_roll'] = pd.Series(data_dict["Inputs"][0])
df['in_pitch'] = pd.Series(data_dict["Inputs"][1])
df['in_yaw'] = pd.Series(data_dict["Inputs"][2])

df['target_xpos'] = pd.Series(data_dict["Target pos"][0])
df['target_ypos'] = pd.Series(data_dict["Target pos"][1])
df['target_zpos'] = pd.Series(data_dict["Target pos"][2])


df['payload_temp'] = pd.Series(data_dict["Payload temp"])
df['energy'] = pd.Series(data_dict["Energy"])
df['adcs_mode'] = pd.Series(data_dict["ADCS mode"])
df['payload_mode'] = pd.Series(data_dict["Payload mode"])

df.to_csv("data/data_orbital.csv")
new_df.to_csv("data/target_info_orbital.csv")
fixed_df.to_csv("data/fixed_data_orbital.csv")
corners_df.to_csv("data/map_corners_orbital.csv")