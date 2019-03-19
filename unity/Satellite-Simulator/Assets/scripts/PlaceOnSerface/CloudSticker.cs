using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;

public class CloudSticker : MonoBehaviour
{
    private float latTopLeft = 0;
    private float longTopLeft = 0;

    private float latBotRight = 0;
    private float longBotRight = 0;

    public float width;
    public float height;

    private string path;

    public float EarthSize;

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        this.gameObject.transform.LookAt(transform.parent.position);
    }

    // Setter for the path of the image.
    // Also load the image at the path to be the sprite as well.
    public void setPath(string imagepath)
    {
        this.path = imagepath;
        this.GetComponent<SpriteRenderer>().sprite = LoadSprite(this.path);
    }

    // Load the image from that path and then it into a sprite.
    private Sprite LoadSprite(string path)
    {
        if (string.IsNullOrEmpty(path)) return null;
        if (System.IO.File.Exists(path))
        {
            byte[] bytes = System.IO.File.ReadAllBytes(path);
            Texture2D texture = new Texture2D(1, 1);
            texture.LoadImage(bytes);
            Sprite sprite = Sprite.Create(texture, new Rect(0, 0, texture.width, texture.height), new Vector2(0.5f, 0.5f));
            return sprite;
        }
        return null;
    }

    // Turn from degree to radian angle measurement.
    float DegToRad(float deg)
    {
        float temp;
        temp = (deg * (float)Mathf.PI) / 180.0f;
        temp = Mathf.Tan(temp);
        return temp;
    }

    // Set latitude and longitude and also adjust each image's width and height.
    public void setLatLong(float latTopLeft, float longTopLeft, float latBotRight, float longBotRight,float widthDivider,float heightDivider, float curvemultiplyer)
    {
        this.latTopLeft = latTopLeft;
        this.longTopLeft = longTopLeft;

        this.latBotRight = latBotRight;
        this.longBotRight = longBotRight;

        this.width = (getWidth() / widthDivider) * (Mathf.Abs(Mathf.Abs((latTopLeft + latBotRight) / 2) - curvemultiplyer) / 14.3f);
        this.height = getHeight() / heightDivider;

        //this.transform.localScale = new Vector3(this.width / 10, this.height / 10, this.transform.localScale.z);
        this.transform.localScale = new Vector3(this.width / (float)12742, this.height / (float)12742, 0);
        this.stickToTarget(EarthSize);
    }

    // Get the distance between 2 lat/lon coordinates.
    public float getDistance()
    {
        double radius = 6371.01;

        Quaternion q1 = Quaternion.Euler(longTopLeft, latTopLeft, 0);
        Quaternion q2 = Quaternion.Euler(longBotRight, latBotRight, 0);
        print(Quaternion.Angle(q1, q2));
        double theta = Quaternion.Angle(q1, q2) * Mathf.Deg2Rad;
        return (float)(radius * theta);
    }

    // Get width from the left and right lattidue
    public float getWidth()
    {
        double radius = 6371.01;

        Quaternion q1 = Quaternion.Euler(longTopLeft, latTopLeft, 0);
        Quaternion q2 = Quaternion.Euler(longTopLeft, latBotRight, 0);
        print(Quaternion.Angle(q1, q2));
        double theta = Quaternion.Angle(q1, q2) * Mathf.Deg2Rad;
        return (float)(radius * theta);
    }

    // Get width from the left and right longitude.
    public float getHeight()
    {
        double radius = 6371.01;

        Quaternion q1 = Quaternion.Euler(longTopLeft, latTopLeft, 0);
        Quaternion q2 = Quaternion.Euler(longBotRight, latTopLeft, 0);
        print(Quaternion.Angle(q1, q2));
        double theta = Quaternion.Angle(q1, q2) * Mathf.Deg2Rad;
        return (float)(radius * theta);
    }

    // This function will transform latitude and longitude into xyz coordinate and stick the image to the Earth.
    void stickToTarget(float sphereRadius)
    {
        //Vector3 targetPosition = Quaternion.AngleAxis(longitude, -Vector3.up) * Quaternion.AngleAxis(latitude, -Vector3.right) * new Vector3(0, 0, sphereRadius);
        //this.gameObject.transform.position = targetPosition + target.position;

        Vector3 position1 = Quaternion.AngleAxis(longTopLeft, -Vector3.up) * Quaternion.AngleAxis(latTopLeft, -Vector3.right) * new Vector3(0, 0, sphereRadius);
        Vector3 position2 = Quaternion.AngleAxis(longBotRight, -Vector3.up) * Quaternion.AngleAxis(latBotRight, -Vector3.right) * new Vector3(0, 0, sphereRadius);

        float x = (position1.x + position2.x) / 2;
        float y = (position1.y + position2.y) / 2;
        float z = (position1.z + position2.z) / 2;


        Vector3 positionCenter = new Vector3(x, y, z);
        this.transform.position = positionCenter;
        //this.gameObject.transform.position = position1 + this.transform.parent.transform.position;
    }
}
