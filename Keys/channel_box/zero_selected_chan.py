# Zero selected channels

import maya.cmds as mc
import maya.mel as mel

sel = mc.ls(sl=1)
channels = mel.eval('selectedChannelBoxAttributes;')
current_time = mc.currentTime(q=1)

for obj in sel:
    for chan in channels:
        mc.setAttr(obj + "." + chan, 0)
