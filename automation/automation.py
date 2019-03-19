import os
import numpy as np

POSSI_LAT = [i for i in range(-90,91,15)]
print(POSSI_LAT)
POSSI_LON = [i for i in range(-180,181,30)]
print(POSSI_LON)

def cartesian_to_polar(x,y,z):

    long = np.arctan2(x,z)

    xzLen = np.sqrt(x**2 + z**2)
    lat = np.arctan2(-y,xzLen)

    lat = np.rad2deg(lat)
    long = np.rad2deg(long)

    return np.array([lat,long])

os.chdir("../python/")
os.system("python3.6 parse_the_orbital_data.py")
os.chdir("../automation/")
os.system("mv ../python/data/data_orbital.csv ./data.csv")

sate_data = np.loadtxt(open("data.csv", "r"), delimiter=",", skiprows=1,usecols=range(5))
print("Load data with :",sate_data.shape)
sate_data = sate_data[:,2:5]

all_coor = cartesian_to_polar(sate_data[:,0],sate_data[:,1],sate_data[:,2])
print("Converted to lat lon:",all_coor.shape)



def generate_load_image_command(coor):

    download_command = []

    for i in range(len(coor[0])):

        coor_ranges = []
        for lat in range(len(POSSI_LAT) - 1):
            if (POSSI_LAT[lat] <= coor[0, i] and coor[0, i] <= POSSI_LAT[lat + 1]):
                coor_ranges.append(POSSI_LAT[lat])
                coor_ranges.append(POSSI_LAT[lat + 1])
                break

        for lon in range(len(POSSI_LON) - 1):
            if (POSSI_LON[lon] <= coor[1, i] and coor[1, i] <= POSSI_LON[lon + 1]):
                coor_ranges.append(POSSI_LON[lon])
                coor_ranges.append(POSSI_LON[lon + 1])
                break

        if(len(coor_ranges) == 4):
            download_command.append(coor_ranges)
        else:
            print("Warning : invalid Coordinate",coor[0, i],coor[1, i])


    return np.array(download_command)

download_command = generate_load_image_command(all_coor)
download_command = np.unique(download_command, axis = 0)
print("Download commands complete:\n", download_command)

for com in download_command:
    os.system("python3.6 satellite_image_request.py --util download --coords ' " + str(com[2]) + "," + str(com[1]) + "," + str(com[3]) + "," + str(com[0]) + "' --time latest --grid 10,10 --maxcc 0.6 --instance-id '11fde559-8832-45bb-87be-c20f0acf48e9'")
