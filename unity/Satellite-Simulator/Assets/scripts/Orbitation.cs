
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System.Collections;

public class Orbitation : MonoBehaviour {

    public Transform centerObject;

    public Slider radiusSlider;
    public Camera mainCamera;

    public double xSpread;
    public double zSpread;
    public double yOffset;

    public float rotSpeed;
    public bool clockwise;

    float timer = 0;


	// Use this for initialization
	void Start () {
        Application.targetFrameRate = 60;
    }
	
	// Update is called once per frame
	void Update () {
        timer += Time.deltaTime * rotSpeed;
        Rotate();
	}

    void Rotate()
    {
        // mainCamera.fieldOfView = 100 * radiusSlider.value;
        if (clockwise)
        {
            double x = -Mathf.Cos(timer) * xSpread;
            double z = Mathf.Sin(timer) * zSpread;
            Vector3 pos = new Vector3((float)x, (float)yOffset, (float)z);
            transform.position = pos + centerObject.position;
        }
        else
        {
            double x = Mathf.Cos(timer) * xSpread;
            double z = Mathf.Sin(timer) * zSpread;
            Vector3 pos = new Vector3((float)x * radiusSlider.value + 250, (float)yOffset * radiusSlider.value + 250, (float)z);
            transform.position = pos + centerObject.position;
        }
    }
}
