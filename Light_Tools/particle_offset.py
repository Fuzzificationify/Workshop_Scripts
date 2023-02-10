import maya.cmds as mc

weight_att = 0.3
smooth_att = 1

min_time = mc.playbackOptions(q=1, minTime=1)
max_time = mc.playbackOptions(q=1, maxTime=1)
time_range = min_time, max_time

sel = mc.ls(sl=1)[0]
sel_matrix = mc.getAttr(sel + ".worldMatrix", time=min_time-50)
sel_trans = (sel_matrix[-4], sel_matrix[-3], sel_matrix[-2])

emitr = mc.emitter(pos=sel_trans)
parti_tran, parti = mc.particle()
mc.connectDynamic(parti, em=emitr)
mc.goal(parti, goal=sel, weight=weight_att, useTransformAsGoal=1)

mc.setAttr(parti + ".maxCount", 1)
mc.setAttr(parti + ".goalSmoothness", smooth_att)
mc.setAttr(parti + ".startFrame", min_time-50)
mc.playbackOptions(minTime=min_time-50)

temp_loc = mc.spaceLocator()[0]
mc.connectAttr(parti + ".worldCentroid", temp_loc + ".translate")

mc.bakeResults(temp_loc, simulation=1, time=(min_time-50, max_time))

mc.delete(emitr, parti_tran)

mc.playbackOptions(animationStartTime=min_time)


# Copy New Animation to Anim Layer
mc.copyKey(temp_loc, attribute=('translate'))
layer_name = sel + "_aLyr"
if mc.objExists(layer_name):
    layer_name = layer_name + "1"

mc.animLayer(layer_name)
mc.select(sel, replace=True)
mc.animLayer(layer_name, e=1, addSelectedObjects=1, override=1)

mc.pasteKey(sel, animLayer=layer_name)



