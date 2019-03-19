using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using NUnit.Framework;

public class FileReaderTest
{
    [Test]
    public void readLogFormat_Test() {
        string fileData = "0\t[\"Hello World\", \"Hello2\"]\t[None, \"colour=red\"]\n";
        fileData += "1.0\t[\"second line\"]\t[\"scale=1.3\"]\n";
        fileData += "2\t[\"third line\"]\t[\"scale=1.3\"]\n";

        List<float> timeStamps = new List<float>();
        List<string> texts = new List<string>(), formats = new List<string>();

        FileReader.readLogFormat(fileData, timeStamps, texts, formats);

        Assert.That(timeStamps.Count, Is.EqualTo(3));
        Assert.That(timeStamps[1], Is.EqualTo(1.0f));
        Assert.That(timeStamps[2], Is.EqualTo(2.0f));
        Assert.That(texts[0], Is.EqualTo("\"Hello World\", \"Hello2\""));
        Assert.That(texts[1], Is.EqualTo("\"second line\""));
        Assert.That(formats[2], Is.EqualTo("\"scale=1.3\""));
    }

    private string generateRow(int b, int column) {
        string line = b.ToString();
        for (int i = 1; i < column; i++) {
            line += "," + (b * 10000).ToString();
        }
        return line + "\n";
    }

    [Test]
    public void readDataCSVFormat_Test() {
        int dataPerRow = 2;
        List<SatellitePosition> positions = new List<SatellitePosition>();
        string fileData = ",time,xpos,ypos,zpos,xdot,ydot,zdot,roll,pitch,yaw,ang_roll,ang_pitch,ang_yaw,in_roll,in_pitch,in_yaw,target_xpos,target_ypos,target_zpos,payload_temp,energy,adcs_mode,payload_mode\n";
        int completeRows = 4, column = 24;
        for (int i = 0; i < completeRows; i++) {
            fileData += generateRow(i, column); 
        }
        fileData += "0,0,0,0,0,0,0,0, , , , , , , , \n";

        FileReader.readDataCSVFormatWithSmoothing(fileData, dataPerRow, positions);

        Assert.That(positions.Count, Is.EqualTo((completeRows - 1) * dataPerRow));
        Assert.That(positions[1].getTime(), Is.EqualTo(10000 / (float) dataPerRow));
        Assert.That(positions[3].getTime(), Is.EqualTo(30000 / (float) dataPerRow));
        Assert.That(positions[4].getPosition(), Is.EqualTo(new Vector3(2.0f, 2.0f, 2.0f)));
        Assert.That(positions[5].getPosition(), Is.EqualTo(new Vector3(2.5f, 2.5f, 2.5f)));
    }
}
