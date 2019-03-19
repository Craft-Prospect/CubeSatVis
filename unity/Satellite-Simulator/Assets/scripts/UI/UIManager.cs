using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class UIManager : MonoBehaviour
{
    public RectTransform satelliteCamPanel;
    public Screen screen;
    // Start is called before the first frame update
    void Start()
    {
    }

    void Update() {
        // float maxWidth = Screen.width, maxHeight = Screen.height;
        // float x = maxWidth - satelliteCamPanel.rect.width - 15,
        //     y = maxHeight - satelliteCamPanel.rect.height - 15;

        // print(maxWidth);
        // print(maxHeight);
        // satelliteCamPanel.anchoredPostion = new Vector2(x, y);
        // satelliteCamPanel.transform.x = x;
        // satelliteCamPanel.transform.y = y;
    }
}
