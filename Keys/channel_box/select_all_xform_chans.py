# Select all transform channels

import maya.cmds as mc

sel = mc.ls(sl=1)

appendix = ['.tx', '.ty', '.tz', '.rx', '.ry', '.rz']
objs_chans_list = []

for obj in sel:
    for chan in appendix:
        objs_chans_list.append(obj + chan)

mc.channelBox('mainChannelBox', edit=1, select=objs_chans_list)
