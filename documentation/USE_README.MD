## Requirements

### Unity version

The Unity version used for this project is `2018.3.1f1`.

### Python version and pip

`Python 3.6` <br/>
`pip`

### Python dependencies

This project has some libraries that it requires and they can be found in `requirements.txt` file. To install these dependencies run the following command:
```
pip install -r requirements.txt
```

## Data Parsing

A `.npy` data input file has to be provided. It should have the same structure as `save_data_qkd.npy` as defined in the README. 

Then our parser `parse_to_csv.py` runs and transforms this data into a .csv file which is ready to be injected into our Unity project.

## Downloading Sentinel-2 Images

A Command Line Interface (CLI) exists for downloading satellite imagery which is mapped to the Earth model. This CLI is in the `sentinelhubcli` project. The CLI takes in several command line arguments which can be displayed using: 

```python3.6 satellite_image_request.py -h```

An example run command is shown below:

```python3.6 satellite_image_request.py --util=download --coords='-86.32,36.65,-90.25,40.245' --time=latest --grid=20,20 --maxcc=0.4 --instance-id youridhere```

The `sentinelhub` package used has several limitations. It uses data from the Sentinel-2 satellite, which has a relatively low-frequency orbit time (5 days). Also, the area specified by `--coords` is split into a grid of images, the dimensions are specified by `--grid`. From extensive testing, it would appear a single image can span a difference of `0.2` in latitude and longitude. If the grid dimensions are too small, a lot of the imagery downloaded will be transparent, which correlates to the specified imagery data not being available.

The CLI is a standalone product which is in a separate project: `sentinelhubcli`



## Including additional text during the visualisation

A CSV file can be place in the “unity/Satellite-Simulation/Assets/data”, it has to be in following format. Then 

Time (float)	Texts (list of strings)	Formats (list of strings)

T1  [“string-11”, “string-12”]  [“modifier-111=value-111 modifier-112=value-112”, “modifier-121=value-121”] <br/>
T2   [“string-21”, “string-22”]   [“modifier-211=value-211”, None] <br/>
. <br/>
. <br/>
. <br/>
Tn   [“string-n1”]   [“modifier-n11=value-n11 modifier-112=value-112”, “modifier-121”] <br/>

-Columns are separated by a tab (‘\t’) <br/>
-Text and Format are always contained in [] brackets <br/>
-Values in a bracket are separated by comma <br/>
-For “Format” items, each field is separated by space and there should not be a space between field, equal sign and value <br/>
-Maximum of 4 texts per row <br/>



## Automation
To automate, build the application using Unity. Then follows these steps.

<img src="documentation/images/automation0.png" width="400">

### Step 1
Go to the `automation` folder.
<img src="documentation/images/automation1.png" width="1000">

### Step 2
Move the builted version of the application to the folder and copy everything inside that folder in to the automation file.
<img src="documentation/images/automation2.png" width="600">
<img src="documentation/images/automation3.png" width="600">

### Step 3
Finally, in the command line, use `Python3.6` to execute the `automation.py` script, which will generate both the images and the `data.csv` file nessesary for the application then launch `Satellite Simulator.exe` as well.
```
python3.6 automation.py
```
If you already have all the images and data.csv, then just launch `Satellite Simulator.exe` directly.


## License
MIT License
