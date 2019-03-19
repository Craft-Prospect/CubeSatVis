using System.Collections;
using System.Collections.Generic;
using System.IO;
using UnityEngine;
using System.Diagnostics;


public class Atmosphere : MonoBehaviour
{

    public string datapath;

     
    public CloudSticker SampleCloudSticker;


    // Start is called before the first frame update
    void Start()
    {
        string path = Application.dataPath;

        while (path.Length > 0 && path[path.Length - 1] != '/')
        {
            path = path.Substring(0, path.Length - 1);
        }
        this.datapath = path + "data";

        //pip install sentinelhub --upgrade
        //ShellHelper.ShellRequest req = ShellHelper.ProcessCommand("python satellite_image_request.py --util download --coords ' 95.751672,20.267350, 104.712596,5.752640' --time latest --grid 10,10 --maxcc 0.8", "");
        //ShellHelper.ShellRequest req = ShellHelper.ProcessCommand("python3 --version", "");

        CloudGroupCoordinate cloud1 = new CloudGroupCoordinate(-75, -90);
        cloud1.setWidthHeightDivider(11f, 10.7f);
        cloud1.curvePortion = 90f;
        cloud1.atmosphereRef = this;
        cloud1.datapath = this.datapath;
        cloud1.loadCloud();
         
        CloudGroupCoordinate cloud2 = new CloudGroupCoordinate(-60,-75);
        cloud2.setWidthHeightDivider(11f, 10.7f);
        cloud2.curvePortion = 90f;
        cloud2.atmosphereRef = this;
        cloud2.datapath = this.datapath;
        cloud2.loadCloud();

        CloudGroupCoordinate cloud3 = new CloudGroupCoordinate(-45, -60);
        cloud3.setWidthHeightDivider(17.5f, 10.7f);
        cloud3.curvePortion = 110f;
        cloud3.atmosphereRef = this;
        cloud3.datapath = this.datapath;
        cloud3.loadCloud();

        CloudGroupCoordinate cloud4 = new CloudGroupCoordinate(-30, -45);
        cloud4.setWidthHeightDivider(16.8f, 10.7f);
        cloud4.curvePortion = 110f;
        cloud4.atmosphereRef = this;
        cloud4.datapath = this.datapath;
        cloud4.loadCloud();

        CloudGroupCoordinate cloud5 = new CloudGroupCoordinate(-15, -30);
        cloud5.setWidthHeightDivider(19.4f, 10.7f);
        cloud5.curvePortion = 120f;
        cloud5.atmosphereRef = this;
        cloud5.datapath = this.datapath;
        cloud5.loadCloud();

        CloudGroupCoordinate cloud6 = new CloudGroupCoordinate(0, -15);
        cloud6.setWidthHeightDivider(28f, 10.7f);
        cloud6.curvePortion = 160f;
        cloud6.atmosphereRef = this;
        cloud6.datapath = this.datapath;
        cloud6.loadCloud();

        this.transform.Rotate(0, -180, 0, Space.Self);

    }

    // Update is called once per frame
    void Update()
    {
        
    }

    // This function will create a CloudSticket object, then stick it to the Admosphere's parent or the Earth.
    // - Input filepath for image, filename for lat and lon, widthdivide and heightdivide resize the image , and curvePortion to match the earth's curve.
    public void loadCloud(string filepath,string filename,float widthdivide,float heightdivide, float curvePortion)
    {
        string[] filenameToken = filename.Split('_');

        CloudSticker cloud = Instantiate(SampleCloudSticker, new Vector3(0, 0, 0), transform.rotation) as CloudSticker;
        cloud.transform.parent = this.transform.parent;


        cloud.setLatLong(float.Parse(filenameToken[4]), float.Parse(filenameToken[3]), float.Parse(filenameToken[6]), float.Parse(filenameToken[5]), widthdivide, heightdivide, curvePortion);
        cloud.setPath(filepath);
    }
}




public class CloudGroupCoordinate
{

    // The latitude of the clouds.
    // latitude change the with of each could sticker, so only latitude is needed.
    public float latTopLeft;
    public float latBotRight;

    // These 2 are used to adjust the lenght and height of each cloud.
    public float widthDivider;
    public float heightDivider;

    // This variable is used to adjust each image's widht as they get put on the earth.
    public float curvePortion;

    // The reference of the atmosphere.
    public Atmosphere atmosphereRef;
    // The location of the cloud's images.
    public string datapath;

    // Constuction, receive 2 latitudes.
    public CloudGroupCoordinate(float _latTopLeft, float _latBotRight)
    {
        this.latTopLeft = _latTopLeft;

        this.latBotRight = _latBotRight;
    }

    // setter for widthDivider and height Divider.
    public void setWidthHeightDivider(float widthDivide, float heightDivide)
    {
        this.widthDivider = widthDivide;
        this.heightDivider = heightDivide;
    }

    // the function that check if the latitude is between left and right latitude.
    public bool isInRange(float latitude)
    {
        //(0, -60, 30, -75);
        if (this.latBotRight <= latitude && this.latTopLeft >= latitude)
        {
            return true;
        }
        else if (-this.latBotRight >= latitude && -this.latTopLeft <= latitude)
        {
            return true;
        }
        return false;
    }

    // Read all the files from the datapath, select the clouds that are between 2 latitude and longitude specified in the constructor.
    // Then create a cloud using loadCloud().
    public void loadCloud()
    {
        var info = new DirectoryInfo(this.datapath);
        var fileInfo = info.GetFiles();
        for (int i = 0; i < fileInfo.Length; i++)
        {
            string[] filenameToken = fileInfo[i].Name.Split('_');

            if(isInRange(float.Parse(filenameToken[4])))
            {

                if (isInRange(float.Parse(filenameToken[6])))
                {

                    string filepath = fileInfo[i].DirectoryName;
                    if (filepath[filepath.Length - 1] != '/')
                    {
                        filepath = filepath + "/";
                    }
                    filepath = filepath + fileInfo[i].Name;

                    this.atmosphereRef.loadCloud(filepath, fileInfo[i].Name, widthDivider, heightDivider, curvePortion);
                }
            }
        }
    }
}



