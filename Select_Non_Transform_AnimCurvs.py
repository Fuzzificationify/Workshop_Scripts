import maya.cmds as mc

animCurveNames = mc.keyframe(q=1, n=1)

noTransform = []

for item in animCurveNames:
    if "translate" not in item and \
        "rotateX" not in item and \
        "rotateY" not in item and \
        "rotateZ" not in item:
        noTransform.append(item)

#Clear Graph Selection
mc.selectionConnection('graphEditor1FromOutliner', e=1, clear=1)

#Select all non-transform animCurves
for each in noTransform:
    selection = mc.selectionConnection('graphEditor1FromOutliner', e=1, select=each)
