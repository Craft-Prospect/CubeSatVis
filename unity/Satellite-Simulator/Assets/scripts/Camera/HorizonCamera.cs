using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;

public class HorizonCamera : MonoBehaviour
{
    public DataManager dataManager;
    private float scale = 1.005f;
    private int iterationOffset = 20 * 12;
    private Vector3 scaleVector, offsetVector, target;
    // Start is called before the first frame update
    void Start()
    {
        scaleVector = new Vector3(scale, scale, scale);
        offsetVector = new Vector3(0, 0, 0);
        target = new Vector3(0, 0, 0);
    }

    // Update is called once per frame
    void Update()
    {
        int currentIndex = dataManager.getIterator();
        int previousIndex = currentIndex - iterationOffset,
            forwardIndex = currentIndex + iterationOffset;
        Vector3 currentPos = dataManager.getCurrentPosition();

        if (!dataManager.validIndex(previousIndex))
        {
            Vector3 backwardPosition = currentPos - (dataManager.getPositionAt(forwardIndex) - currentPos);

            transform.position = Vector3.Scale(backwardPosition, scaleVector);
        }
        else
        {
            transform.position = Vector3.Scale(dataManager.getPositionAt(previousIndex), scaleVector);
        }

        transform.LookAt(currentPos);

    }
}
