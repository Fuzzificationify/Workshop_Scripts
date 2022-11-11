# Set the current time to selected keyframe

sel_key = sorted(mc.keyframe(q=1, selected=1))
min_key, max_key = sel_key[0], sel_key[-1]

current_time = mc.currentTime(q=1)
 
min_dif = abs(min_key - current_time)
max_dif = abs(max_key - current_time)

if min_dif >= max_dif:
    print('min_key')
    mc.currentTime(max_key)
    
if min_dif < max_dif:
    print('max_key')
    mc.currentTime(min_key)
