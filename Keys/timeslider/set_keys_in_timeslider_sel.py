# Set Insert Keys in frame range

sel = mc.ls(sl=1)

aTimeSlider = mel.eval('$tmpVar=$gPlayBackSlider')
timeRange = mc.timeControl(aTimeSlider, q=True, rangeArray=True)
start, end = timeRange[0], timeRange[1]

for i in range(int(start), int(end)):
    mc.setKeyframe(sel, time=(i, i), insert=1)
