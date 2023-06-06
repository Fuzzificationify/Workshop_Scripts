# Sometimes when baking a certain frame range Maya will delete the existing out-of-range keys.
# This script extracts the existing animation first to protect it.

# Because the script just copies keys it will only work on objs in the same space

import maya.cmds as mc

sel = mc.ls(sl=1)
animLayer_name = sel[0] + "_base"

minTime = mc.playbackOptions(q=1, minTime=1)
maxTime = mc.playbackOptions(q=1, maxTime=1)
time_range = minTime, maxTime

# Extract base animation to new layer
extract_lyr = mc.animLayer(animLayer_name, override=1, addSelectedObjects=1, extractAnimation="BaseAnimation")

mc.bakeResults(sel, time=time_range, bakeOnOverrideLayer=True, preserveOutsideKeys=True)
bake_container = mc.ls(sl=1, type="container")[0]

if mc.animLayer(sel, q=1, affectedLayers=1) and mc.animLayer('BakeResults', q=1, exists=1):
    mc.rename('BakeResults', sel[0] + "_bk_lyr")

# Copy anim back to Base layer and delete
mc.animLayer('BaseAnimation', e=1, copyAnimation=extract_lyr)
mc.delete(extract_lyr) 
