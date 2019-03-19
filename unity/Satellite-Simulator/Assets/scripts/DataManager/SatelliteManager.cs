using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SatelliteManager : MonoBehaviour
{
    public GameObject Satellite;
    public DataManager dataManager;
    private float lasttimer = 0;
    private float durations = 0;
    private Vector3 currentPosition = new Vector3(654, 175, 0);
    public Vector3 position;
    public double time;

    // Start is called before the first frame update
    void Start()
    {
        StartCoroutine(callEverySecond());
    }

    // Update is called once per frame
    void Update()
    {
 
    }

    IEnumerator callEverySecond()
    {
        while (true)
        {
            float compiletime = 0;
            try
            {
                compiletime = continueIterating();
            }
            catch( Exception e )
            {
                
            }
            yield return new WaitForSeconds(durations - compiletime);
           

        }
    }


    float continueIterating()
    {
        float time = Time.time;
        dataManager.iterate();
        print(dataManager.getCurrentTime());
        Debug.LogError("Current x position is " + dataManager.getCurrentPosition().x);
        print("----------------------------------");

        durations = (float)dataManager.getCurrentTime() - lasttimer;
        lasttimer = (float)dataManager.getCurrentTime();
        return Time.time - time;
    }
}
