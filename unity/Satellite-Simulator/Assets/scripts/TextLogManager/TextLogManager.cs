using System.Collections;
using System.Collections.Generic;
using System;
using UnityEngine;
using UnityEngine.UI;

public class TextLogManager : MonoBehaviour
{
    private const int DEFAULT_FONT_SIZE = 14;
    private Dictionary<string, Color> colorMap;
    private int index = -1;
    private List<float> timeStamps;
    private List<string> texts;
    private List<string> formats;

    public string csv_path;
    public DataManager dataManager;

    public Text field1, field2, field3, field4;
    private Text[] textFields;
    void Start()
    {
        textFields = new[] { field1, field2, field3, field4 };
        timeStamps = new List<float>();
        texts = new List<string>();
        formats = new List<string>();
        colorMap = new Dictionary<string, Color>() {
            {"white", Color.white},
            {"red", Color.red},
            {"green", Color.green},
            {"yellow", Color.yellow},
            {"blue", Color.blue},
            {"grey", Color.grey}
        };

        string fileData = System.IO.File.ReadAllText(csv_path);
        FileReader.readLogFormat(fileData, timeStamps, texts, formats);
    }
    // Update is called once per frame
    void Update()
    {
        if (index >= timeStamps.Count - 1) return;
        if (dataManager.getTimer() >= timeStamps[index + 1])
        {
            index++;
            if (index >= timeStamps.Count) return;
            //dataUpdated = true;
            string[] rawTexts = texts[index].Split(","[0]);
            string[] formatting = formats[index].Split(","[0]);

            for (int i = 0; i < textFields.Length; i++)
            {   
                if (i < rawTexts.Length) {
                    String raw = rawTexts[i].Trim();
                    textFields[i].text = raw.Substring(1, raw.Length - 2);
                    if (formatting[i].Trim() != "None") {
                        string trimmed = formatting[i].Trim();
                        trimmed = trimmed.Substring(1, trimmed.Length - 2);
                        formatText(textFields[i], trimmed.Split(" "[0]));
                    } else {
                        textFields[i].fontSize = DEFAULT_FONT_SIZE;
                        textFields[i].color = colorMap["white"];
                    }
                } else {
                    textFields[i].text = "";
                }
            }
        }
    }

    void formatText(Text textObject, string[] options) {
        string colour = "white";
        double scale = 1;
        for (int i = 0; i < options.Length; i++) {
            string option = options[i].Trim();
            if (option.Substring(0, 6) == "colour") colour = option.Substring(7, option.Length - 7);
            if (option.Substring(0, 5) == "scale") scale = double.Parse(option.Substring(6, option.Length - 6));
        }
        if (colorMap.ContainsKey(colour)) {
            textObject.color = colorMap[colour];
        }
        if (scale > 0) {
            textObject.fontSize = (int) Math.Ceiling(DEFAULT_FONT_SIZE * scale);
        }
    }
}
