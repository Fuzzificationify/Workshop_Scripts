import maya.cmds as mc

sel = mc.ls(sl=1)
sel_channels = mc.channelBox('mainChannelBox', q=1, sma=1)

channels_list = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz']
skip_rot = []
skip_tran = []

if sel_channels:
    for channel in channels_list:
        if channel not in sel_channels:
            if channel[0] == 't':
                skip_tran.append(channel[1])
            if channel[0] == 'r':
                skip_rot.append(channel[1])

pCon = mc.parentConstraint(sel[0], sel[1], skipRotate=skip_rot, skipTranslate=skip_tran, mo=0)
