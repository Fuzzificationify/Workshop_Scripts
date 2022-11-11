import maya.cmds as mc

def del_keys_from_channelbox(all=0):
    channels = mc.channelBox('mainChannelBox', q=1, sma=1)
    if all==0:
        time = mc.currentTime(q=1)
    else:
        time = ":"

    mc.cutKey(attribute=channels, time=(time,))
    
    
del_keys_from_channelbox()
