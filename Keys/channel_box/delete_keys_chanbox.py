import maya.cmds as mc
import maya.mel as mel

def del_keys_from_channelbox(all=0):
    # Using mel to catch shape attributes too
    channels = mel.eval('selectedChannelBoxAttributes;')
    if all==0:
        time = mc.currentTime(q=1)
    else:
        time = ":"

    mc.cutKey(attribute=channels, time=(time,))
    
    
del_keys_from_channelbox()
