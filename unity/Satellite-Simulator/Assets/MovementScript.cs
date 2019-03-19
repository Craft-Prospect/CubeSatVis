using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MovementScript : MonoBehaviour
{
    public DataManager dataManager;
    public Vector3 satellitePosition;
    public Vector3 testCoordinate;
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        satellitePosition = dataManager.getCurrentPosition();
    }
}
