min_time = mc.playbackOptions(q=1, minTime=1)
time = mc.currentTime(q=1)

mc.play(state=False) # Stop if playing

if time-24 <= min_time:
    mc.currentTime(min_time)
else:
    mc.currentTime(time-24)
