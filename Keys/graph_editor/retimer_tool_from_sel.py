import maya.cmds as mc

if mc.contextInfo("retimeKey1", exists=1):
    mc.retimeKeyCtx("retimeKey1", e=1)
    mc.setToolTo("retimeKey1")

else:
    mc.retimeKeyCtx("retimeKey1")
    mc.setToolTo("retimeKey1")

key_times = sorted(mc.keyframe(q=1, sl=1))
first_key, last_key = key_times[0], key_times[-1]

first_funky_time = first_key / 24
last_funky_time = last_key / 24
mid_time = (first_funky_time + last_funky_time) / 2

mc.retimeHelper(frame=first_funky_time)
mc.retimeHelper(frame=last_funky_time)
mc.retimeHelper(frame=mid_time)
