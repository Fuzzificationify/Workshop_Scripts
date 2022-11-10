import maya.cmds as mc
import maya.mel as mel

all_panels = mc.getPanel(vis=1)

graph_editors = [pan for pan in all_panels if "graphEditor" in pan]

if graph_editors:
    mc.deleteUI(graph_editors, panel=1)
    
else:
    mel.eval("GraphEditor;")

