import maya.cmds as mc
import maya.mel as mel

focus = mc.getPanel(wf=1)
graphEdit = mc.getPanel(scriptType='graphEditor')

if not graphEdit:
    graphEdit = mel.eval("GraphEditor;")

mc.scriptedPanel(graphEdit[0], edit=1, rp=focus)

mc.animCurveEditor('graphEditor1GraphEd', exists=True)
