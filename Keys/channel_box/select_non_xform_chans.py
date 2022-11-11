# Select all NON-transform channels

import maya.cmds as mc

sel = mc.ls(sl=1)

appendix = ['translateX', 'translateY', 'translateZ',
             'rotateX', 'rotateY', 'rotateZ']
objs_chans_list = []

# Find the non-trans channels
animAttributes = mc.listAnimatable(sel)
anim_attrs = [x.split('.')[-1] for x in animAttributes]
non_trans_attrs = [y for y in anim_attrs if y not in appendix]

for obj in sel:
    for chan in non_trans_attrs:
        objs_chans_list.append(obj + '.' + chan)

mc.channelBox('mainChannelBox', edit=1, select=objs_chans_list)
