using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class LogText : MonoBehaviour
{

    private Text text;
    public DataManager dataManager;
    // Start is called before the first frame update
    void Awake()
    {
        text = GetComponent<Text>();
    }

    // Update is called once per frame
    void Update()
    {
        // Vector3 currentPosition = dataManager.getCurrentPosition();
        // string currentText = "";
        // currentText = currentPosition.ToString();
        // currentText += "\nTime: " + dataManager.getCurrentTime().ToString();
        // text.text = currentText;
    }
}
