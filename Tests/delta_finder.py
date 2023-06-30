import maya.cmds as mc

anim_curve = mc.keyframe(q=1, n=1)
delta_list = []

numKeyframes = mc.keyframe(anim_curve, q=True, keyframeCount=True)
keys = mc.keyframe(anim_curve, q=1, index=(0, numKeyframes), valueChange=1)

for i, val in enumerate(keys):
    delta = keys[(i + 1)] - keys[i]
    delta_list.append(delta)

#Set Keys
for j in range(len(delta_list)):
    mc.setKeyframe('pCube22.rz', time=j, value=delta_list[j])
    # mc.setKeyframe('pSphere1.tz', time=j, value=delta_list[j])
