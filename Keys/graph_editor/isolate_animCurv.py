import maya.cmds as mc
import maya.mel as mel

curveSelection = mc.keyframe(query=True, selected=True, name=True)

if curveSelection:
    mel.eval("isolateAnimCurve true graphEditor1FromOutliner graphEditor1GraphEd")

else:
    mel.eval("isolateAnimCurve false graphEditor1FromOutliner graphEditor1GraphEd")
