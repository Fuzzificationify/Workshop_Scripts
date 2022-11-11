# Zero selected channels

import maya.cmds as mc

sel = mc.ls(sl=1)
channels = mc.channelBox('mainChannelBox', q=1, sma=1)
current_time = mc.currentTime(q=1)

for obj in sel:
    for chan in channels:
        mc.setAttr(obj + "." + chan, 0)


