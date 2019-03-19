using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class LatLongSticker : MonoBehaviour {

    public Transform target;
    public float distanceFromOrigin;

	// Use this for initialization
	void Start () {
        print(target.localScale.x);
    }
	
	// Update is called once per frame
	void Update () {
        stickToTarget((float)13.736717, (float)100.523186, distanceFromOrigin);
        this.gameObject.transform.LookAt(target.position);
    }

    void stickToTarget(float latitude, float longitude, float sphereRadius)
    {
        Vector3 targetPosition = Quaternion.AngleAxis(longitude, -Vector3.up) * Quaternion.AngleAxis(latitude, -Vector3.right) * new Vector3(0, 0, sphereRadius);
        this.gameObject.transform.position = targetPosition + target.position;
    }
}
