import maya.cmds as mc

try:
    if mc.ls(my_panel):
        mc.deleteUI(my_panel, panel=True)
except:
    pass

my_panel = mc.modelPanel(camera="persp")
yep = mc.modelPanel(my_panel, edit=True, replacePanel='graphEditor1')
