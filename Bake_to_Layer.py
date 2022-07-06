import maya.cmds as mc

sel = mc.ls(sl=1)
animLayer_name = sel[0] + "_base"

minTime = mc.playbackOptions(q=1, minTime=1)
maxTime = mc.playbackOptions(q=1, maxTime=1)
time_range = minTime, maxTime

mc.animLayer(animLayer_name, override=1, addSelectedObjects=1, extractAnimation="BaseAnimation")

mc.bakeResults(sel, time=time_range, bakeOnOverrideLayer=True, preserveOutsideKeys=True)

if mc.animLayer(sel, q=1, affectedLayers=1) and mc.animLayer('BakeResults', q=1, exists=1):
    mc.rename('BakeResults', sel[0] + "_bk_lyr")

mc.delete(sel, constraints=True)
