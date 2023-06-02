import maya.cmds as mc
from Helper_Functions import keyframe_helpers as kh

selObj = mc.ls(sl=1)

# Get Time Slider Range
minTime = mc.playbackOptions(q=1, minTime=1)
maxTime = mc.playbackOptions(q=1, maxTime=1)

# Get Keyframe Range
start_keyframe, end_keyframe, _ = kh.get_key_times(selObj, sl_keys=False)

# Find the largest range between Time Slider and Keyframes
if start_keyframe != None:
    start_time = min(minTime, start_keyframe)
    end_time = max(maxTime, end_keyframe)
else:  # If there's no keys
    start_time = minTime
    end_time = maxTime

    # Sets keys on xform channels as mc.bake will only work when there's at least 1 key
    mc.setKeyframe(selObj, t=start_time, respectKeyable=1, at=('t', 'r'))

bake_range = start_time, end_time

# Bake
mc.bakeResults(selObj, t=bake_range)

# Delete Constraint
child_con = mc.listRelatives(selObj, children=1, type='constraint')
mc.delete(child_con, constraints=1)
