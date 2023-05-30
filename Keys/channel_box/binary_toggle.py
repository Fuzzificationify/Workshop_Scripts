import maya.mel as mel
import pymel.core as pm

channels = mel.eval('selectedChannelBoxAttributes;')

sel = pm.ls(sl=1)

for obj in sel:
    for chan in channels:
        value = obj.attr(chan).get(0)
        if value != 0:
            obj.attr(chan).set(0)
        else:
            obj.attr(chan).set(1)
