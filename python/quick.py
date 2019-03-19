import numpy as np

data = np.load("save_data_qkd.npy").item()

new_data = data

del new_data["Data"]["Key delivered"]

print(new_data["Data"].keys())

np.save("save_data_qkd.npy", new_data)
