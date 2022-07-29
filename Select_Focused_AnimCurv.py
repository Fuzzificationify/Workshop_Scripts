import maya.cmds as mc

obj = mc.ls(sl=1)
sel_keys = []

# Checks if there's keys selected
for o in obj:
    sel_chan = mc.keyframe(o, q=1, n=1, sl=1) or None
    if sel_chan != None:
        sel_keys.append(sel_chan)


if sel_keys:
    all_curvs = [x for list in sel_keys for x in list]
    mc.selectKey(all_curvs)

else:
    graphEditorObjects = mc.selectionConnection('graphEditor1FromOutliner', q=1, object=1)
    mc.selectKey(graphEditorObjects)
