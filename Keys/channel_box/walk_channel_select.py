import maya.cmds as mc
import maya.mel as mel

sel = mc.ls(sl=1)


def walk_channel_select(attributes=['tx', 'ty', 'tz']):
    new_sel_list = []
    at_x = attributes[0]
    at_y = attributes[1]
    at_z = attributes[2]

    channels = mel.eval('selectedChannelBoxAttributes;') or None

    # any() bit returns True if there's any channels outside of the attributes list present
    if (channels is None) or any([att for att in channels if att not in attributes]):
        print('in here')
        for ctrl in sel:

            for att in attributes:
                new_sel_list.append(ctrl + "." + att)

        mc.channelBox('mainChannelBox', edit=1, select=new_sel_list)

    elif len(channels) == 3:
        for ctrl in sel:
            mc.channelBox('mainChannelBox', edit=1, select=ctrl + '.' + at_x)

    elif at_x in channels:
        for ctrl in sel:
            mc.channelBox('mainChannelBox', edit=1, select=ctrl + '.' + at_y)

    elif at_y in channels:
        for ctrl in sel:
            mc.channelBox('mainChannelBox', edit=1, select=ctrl + '.' + at_z)

    elif at_z in channels:
        for ctrl in sel:

            for att in attributes:
                new_sel_list.append(ctrl + "." + att)

        mc.channelBox('mainChannelBox', edit=1, select=new_sel_list)

walk_channel_select()
