using System.Collections;
using System.Collections.Generic;
using System;
using UnityEngine;

public class DataManager : MonoBehaviour
{
    public string csv_path;
    private List<SatellitePosition> satellitesPosition;
    private int iterator = 0;
    public GameObject satellite;


    private const float FPS = 24.0f, dataTimeGap = 0.5f;
    private const int generatedDataPerRow = (int)(FPS * dataTimeGap);
    private float simulationTimeGap = dataTimeGap / generatedDataPerRow, timer = 0.0f;

    // Use this for initialization
    void Start()
    {
        print("Warning: \n\t The measurement is 0.1 of the real value. And they are in KM matric. For example the radius of the earth is 637.8 KM");
        this.satellitesPosition = new List<SatellitePosition>();
        string fileData = System.IO.File.ReadAllText(csv_path);
        FileReader.readDataCSVFormatWithSmoothing(fileData, generatedDataPerRow, this.satellitesPosition);
        InvokeRepeating("iterate", 0.0f, simulationTimeGap);
    }

    void Update()
    {
        timer += Time.deltaTime;
    }

    public Vector3 getCurrentPosition()
    {
        return this.satellitesPosition[this.iterator].getPosition();
    }

    public double getCurrentTime()
    {
        return this.satellitesPosition[this.iterator].getTime();
    }

    public bool iterate()
    {
        if (iterator == this.satellitesPosition.Count - 1)
        {
            return false;
        }

        satellite.transform.position = this.satellitesPosition[this.iterator].getPosition();
        satellite.transform.Rotate(this.satellitesPosition[this.iterator].getRotation());

        iterator += 1;
        return true;


    }
    public int getIterator()
    {
        return iterator;
    }

    public bool validIndex(int index)
    {
        return index >= 0 && index < this.satellitesPosition.Count;
    }

    public Vector3 getPositionAt(int index)
    {
        if (validIndex(index)) return this.satellitesPosition[index].getPosition();
        return default(Vector3);
    }

    public float getTimer()
    {
        return timer;
    }
    public float getTimeFraction()
    {
        return (float)(timer - getCurrentTime()) / simulationTimeGap;
    }
}


public class SatellitePosition
{
    private double time;
    private Vector3 position;
    private Vector3 rotation;
    private double roll;
    private double pitch;
    private double yaw;

    public SatellitePosition(double ctime)
    {
        this.time = ctime;
    }

    public void setPosition(float x, float y, float z)
    {
        position = new Vector3(x, y, z);
    }

    public Vector3 getRotation()
    {
        return rotation;
    }

    public void setRotation(float roll, float pitch, float yaw)
    {
        rotation = new Vector3(roll, pitch, yaw);
    }

    public double getRollSpeed()
    {
        return roll;
    }

    public double getPitchSpeed()
    {
        return pitch;
    }

    public double getYawSpeed()
    {
        return yaw;
    }

    public void setRollSpeed(double roll)
    {
        this.roll = roll;
    }

    public void setPitchSpeed(double pitch)
    {
        this.pitch = pitch;
    }

    public void setYawSpeed(double yaw)
    {
        this.yaw = yaw;
    }

    public Vector3 getPosition()
    {
        return position;
    }

    public double getTime()
    {
        return time;
    }
}
