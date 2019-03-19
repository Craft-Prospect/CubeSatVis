using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class TestDataText : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        Text temp = GetComponent<Text>();
        temp.text = Application.dataPath;
        print(Application.dataPath);
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
