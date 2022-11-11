import maya.cmds as mc
my_panel = mc.getPanel(wf=1)

mc.modelEditor(my_panel, e=1, shadows=1)
mc.modelEditor(my_panel, e=1, displayTextures=1)
mc.modelEditor(my_panel, e=1, displayLights='all')

mc.setAttr("hardwareRenderingGlobals.ssaoEnable", 1)
mc.setAttr("hardwareRenderingGlobals.multiSampleEnable", 1)


import maya.cmds as mc
my_panel = mc.getPanel(wf=1)

mc.modelEditor(my_panel, e=1, shadows=0)
mc.modelEditor(my_panel, e=1, displayTextures=0)
mc.modelEditor(my_panel, e=1, displayLights='none')
mc.modelEditor(my_panel, e=1, displayAppearance='smoothShaded')
mc.DisplayShaded()

mc.setAttr("hardwareRenderingGlobals.ssaoEnable", 0)
mc.setAttr("hardwareRenderingGlobals.multiSampleEnable", 0)
