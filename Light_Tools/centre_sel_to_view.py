# Centre selection to current camera
import maya.cmds as mc

sel = mc.ls(sl=1)

current_panel = mc.getPanel(withFocus=1)
cam = mc.modelPanel(current_panel, query=True, camera=True)

mc.parent(sel, cam, relative=1)
mc.xform(sel, t=(0,0,-10))
mc.parent(sel, world=1)
mc.xform(sel, rotation=(0, 0, 0))

#pCon = mc.parentConstraint(cam, sel, mo=0)[0]
#mel.eval('setAttr "{0}.target[0].targetOffsetTranslateZ" -10;'.format(pCon))
#mc.DeleteConstraints(pCon)
