using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class DirectCamera : MonoBehaviour
{
    public DataManager dataManager;
    public float scale;
    private Vector3 earthPosition, scaleVector;
    // Start is called before the first frame update
    void Start()
    {
        earthPosition = new Vector3(0.0f, 0.0f, 0.0f);
        scaleVector = new Vector3(scale, scale, scale);
    }

    void Update()
    {
        transform.position = Vector3.Scale(dataManager.getCurrentPosition(), scaleVector);
        transform.LookAt(earthPosition);
    }
}
