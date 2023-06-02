# Currently only works on time, so if it's not on 1s it's not going to work
# Need to think of a smarter deletion function

from Helper_Functions import keyframe_helpers
reload(keyframe_helpers)

key_selection = 0
graph_curv = mc.keyframe(q=1, n=1, sl=1) or []
sel_channels = mc.channelBox('mainChannelBox', q=1, sma=1)

# TimeSlider check
if keyframe_helpers.check_timeslider_sel():
    start_time, end_time = keyframe_helpers.get_timeslider_sel_range()
    if sel_channels: keys = sel_channels
    else:    
        keys = mc.listAnimatable() # Use on all channels 
    
    key_selection = 1

# Graph Key check
elif mc.keyframe(q=1, sl=1):
    start_time, end_time, _ = keyframe_helpers.get_key_times(graph_curv)
    keys = mc.keyframe(q=1, n=1) # Use on selected key channels
    
    key_selection = 1

# Delete Nth Key
if key_selection:
    for i in range(int(start_time), int(end_time)):
        if (i+2) % 2 != 0:
            mc.cutKey(keys, time=(i,))
