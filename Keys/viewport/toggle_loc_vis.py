import maya.cmds as mc

pan = mc.getPanel(wf=1)

loc_vis = mc.modelEditor(pan, q=1, locators=1)

if loc_vis:
    mc.modelEditor(pan, e=1, locators=0)
else:
    mc.modelEditor(pan, e=1, locators=1)
