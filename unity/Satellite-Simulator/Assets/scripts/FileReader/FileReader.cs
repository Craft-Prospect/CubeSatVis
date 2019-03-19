using System;
using System.Collections;
using System.Collections.Generic;

public class FileReader
{
    public static void readLogFormat(string fileData,
                                    List<float> timeStamps,
                                    List<string> texts,
                                    List<string> formats)
    {
        string[] lines = fileData.Split("\n"[0]);
        for (int i = 0; i < lines.Length; i++)
        {
            string[] lineData = lines[i].Split("\t"[0]);
            if (lineData.Length < 3) break;
            timeStamps.Add(float.Parse(lineData[0]));
            texts.Add(lineData[1].Substring(1, lineData[1].Length - 2));
            formats.Add(lineData[2].Substring(1, lineData[2].Length - 2));
        }
    }

    public static void readDataCSVFormatWithSmoothing(string fileData, int dataPerRow, List<SatellitePosition> satPositions)
    {
        string[] lines = fileData.Split("\n"[0]);
        for (int i = 1; i < lines.Length - 1; i++)
        {
            string[] lineData = (lines[i].Trim()).Split(","[0]);
            string[] nextLineData = (lines[i + 1].Trim()).Split(","[0]);

            try
            {
                float.Parse(nextLineData[8]);
            }
            catch (Exception e)
            {
                break;
            }

            float time1 = float.Parse(lineData[1]), time2 = float.Parse(nextLineData[1]);
            float x1, x2, y1, y2, z1, z2;
            x1 = float.Parse(lineData[2]) / 10000;
            x2 = float.Parse(nextLineData[2]) / 10000;
            y1 = float.Parse(lineData[3]) / 10000;
            y2 = float.Parse(nextLineData[3]) / 10000;
            z1 = float.Parse(lineData[4]) / 10000;
            z2 = float.Parse(nextLineData[4]) / 10000;
            for (int j = 0; j < dataPerRow; j++)
            {

                float timeStamp = time1 + (time2 - time1) * (j / (float)dataPerRow);

                SatellitePosition satellite = new SatellitePosition(timeStamp);
                satellite.setPosition(x1 + (x2 - x1) * (j / (float)dataPerRow),
                                      y1 + (y2 - y1) * (j / (float)dataPerRow),
                                      z1 + (z2 - z1) * (j / (float)dataPerRow));
                float xAngle = (float)Math.Cos(float.Parse(lineData[11])) * (float)Math.Cos(float.Parse(lineData[10]));
                float yAngle = (float)Math.Sin(float.Parse(lineData[11])) * (float)Math.Cos(float.Parse(lineData[10]));
                float zAngle = (float)Math.Sin(float.Parse(lineData[10]));
                satellite.setRotation(xAngle / 57, yAngle / 57, zAngle / 57); // VERY INEXACT CONVERSION
                satPositions.Add(satellite);
            }

        }
    }

}