using System;
using NUnit.Framework;

public class TestCloudGroupCoordinate
{
    CloudGroupCoordinate cloud1;

    [OneTimeSetUp]
    public void createMockCloudGroupCoordinate()
    {
        cloud1 = new CloudGroupCoordinate(-75, -90);
        cloud1.setWidthHeightDivider(11f, 10.7f);
        cloud1.curvePortion = 90f;
    }

    [Test]
    public void isInRangeTrue()
    {
        Assert.True(cloud1.isInRange(80));
    }

    [Test]
    public void isInRangeFalse()
    {
        Assert.False(cloud1.isInRange(-65));
    }
}
