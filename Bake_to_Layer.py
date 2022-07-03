import maya.cmds as mc

sel = mc.ls(sl=1)
animLayer_name = sel[0] + "_base"

mc.animLayer(animLayer_name, override=1, addSelectedObjects=1, extractAnimation="BaseAnimation")

mc.bakeResults(sel, time=(10, 100), bakeOnOverrideLayer=True, preserveOutsideKeys=True)

if mc.animLayer(sel, q=1, affectedLayers=1) and mc.animLayer('BakeResults', q=1, exists=1):
    mc.rename('BakeResults', sel[0] + "_bk_lyr")

mc.delete(sel, constraints=True)
