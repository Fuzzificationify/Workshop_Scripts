import maya.cmds as mc

if mc.keyframe(q=1, sl=1):
    animCurveNames = mc.keyframe(q=1, n=1)
    mc.selectKey(animCurveNames)

else:
    graphEditorObjects = mc.selectionConnection('graphEditor1FromOutliner', q=1, object=1)
    mc.selectKey(graphEditorObjects)
