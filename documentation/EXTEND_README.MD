## Earth model
For now, Earth is quite highly-polygonal model with a relatively low quality map. Problem is, for up to 16k there is no visible difference for the visualisation, and above that - there are no such free maps and they are going to slow down loading as well. However, if desired to replace the texture, first add it to unity assets by copying into “Assets” folder and then dragging and dropping into Earth_2_fbx’s child “Earth_Map”

![img1](documentation/images/pasted_image_0.png)


## Using different dataset
In order to use set of data, different from data_orbital, make sure it’s in the right format (.csv) by running it through the data parser (located in /python/parse_the_orbital_data.py). To do that, replace save_data_orbital.npy in line 5 by desired data file name and names in lines 62-65 by the desired output names.
After that, specify new data file in the Data Manager, see picture in the “Satellite” paragraph.

## Satellite
In order to replace/modify satellite’s model simply remove the old one in the Main level, load the new prefab and replace reference in the DataManager, part “Satellite” (see below).

![img1](documentation/images/pasted_image_1.png)



## Downloading satellite imagery

The current process uses a command-line interface to download images from the Sentinel-2 satellite by utilising the sentinelhub package. However there are numerous bottlenecks associated with using this package. 

With a free Sentinel-hub account, the user is permitted to 10,000 image downloads per day. This is not scalable to our use case as:
The images are taken from a relatively low height, meaning an image can only span a difference of 0.2 in latitude and longitude. Since the CubeSat orbit spans the majority of the globe, this would mean downloading an unfeasible amount of images both in terms of time, download limitations, and rendering capabilities of a relatively powerful PC. There may be more features available with a paid Enterprise account, however this was not available to us. 

The CLI can be improved by changing from argparse to Click 7.0.0. This is a slicker commandline interface with better formatted help text and extra functionality.

The CLI is a standalone product and is in a separate project: `sentinelhubcli`


## Testing 

The current project includes unit test scripts for non-Monobehaviour classes (Unity’s environment independent classes). Details on Monobehaviour test development can be found [here](https://blogs.unity3d.com/2014/06/03/unit-testing-part-2-unit-testing-monobehaviours/).

Test modules can be added to the project by placing C# scripts in the directory “./Assets/scripts/Editor/”. Unity then will automatically detect the script. The test can now be execute via Unity’s interface by going to Window >> General >> Test Runner.

<img src="documentation/images/pasted_image_2.png" width="200">                <img src="documentation/images/pasted_image_3.png" width="200">

All test functions with a valid syntax and format should appear and “Run All” or “Run Selected” can be used to start the test. Successful tests will be marked with green check while failed ones
Are shown as forbidden sign. 

