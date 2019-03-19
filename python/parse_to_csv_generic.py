import numpy as np
import pandas as pd


data = np.load('save_data_qkd.npy')
data_dict = data.item()["Data"]
corners_list = data.item()["Corners"]

time_step = data_dict["Time step"]; del data_dict["Time step"]
target_info = data_dict["Target info"]; del data_dict["Target info"]
adcs_mode_names = data_dict["ADCS mode names"]; del data_dict["ADCS mode names"]
payload_mode_names = data_dict["Payload mode names"]; del data_dict["Payload mode names"]

fixed_df = pd.DataFrame()
fixed_df['time_step'] = pd.Series(time_step)
fixed_df['adcs_mode_names'] = pd.Series(adcs_mode_names[0])
fixed_df['payload_mode_names'] = pd.Series(payload_mode_names[0])

df = pd.DataFrame()
new_df = pd.DataFrame.from_dict(target_info)
corners_df = pd.DataFrame()
corners_df["bottom_left"] = pd.Series(corners_list[0])
corners_df["bottom_right"] = pd.Series(corners_list[1])
corners_df["top_right"] = pd.Series(corners_list[2])
corners_df["top_left"] = pd.Series(corners_list[3])

xyz_dict = {k: v for k, v in data_dict.items() if len(data_dict[k])==3}
clean_dict = {k: v for k, v in data_dict.items() if len(data_dict[k])==1876}

for k, v in clean_dict.items():
    df[k] = pd.Series(v)

for k, v in xyz_dict.items():
    df[k + "_1"] = pd.Series(v[0])
    df[k + "_2"] = pd.Series(v[1])
    df[k + "_3"] = pd.Series(v[2])

df.to_csv("data_gen.csv")
new_df.to_csv("target_info_gen.csv")
fixed_df.to_csv("fixed_data_gen.csv")
corners_df.to_csv("map_corners_gen.csv")