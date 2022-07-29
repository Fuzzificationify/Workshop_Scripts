import maya.cmds as mc

def if_animCurvs_sel(animCurvs):
    channels_list = []
    if animCurvs:
        for curv in animCurvs:
            just_channel = curv.replace('_', '.')
            channels_list.append(just_channel)

        return channels_list

def if_graphChannel_sel(graph_channels, objs):
    channels_list = []
    if graph_channels:
        for channel in graph_channels:
            channels_list.append(channel)

        return channels_list

def if_sel_channels(sel_channels, obj):
    channels_list = []
    if sel_channels:
        for channel in sel_channels:
            o_channel = obj + '.' + channel
            channels_list.append(o_channel)

        return channels_list

def mute_logic(channels):
    is_mute = mc.mute(channels[0], q=1)
    for channel in channels:
        if is_mute == False:
            mc.mute(channel)

        else:
            mc.mute(channel, disable=1)


def main():
    objs = mc.ls(sl=1)

    animCurvs = mc.keyframe(objs[0], q=1, n=1, sl=1)

    graph_channels = mc.selectionConnection('graphEditor1FromOutliner', q=1, object=1)
    sel_channels = mc.channelBox('mainChannelBox', q=1, sma=1)

    if (len(objs) < 1):
        return

    for each in objs:
        if animCurvs:
            channels_list = if_animCurvs_sel(animCurvs)

        elif graph_channels:
            channels_list = if_graphChannel_sel(graph_channels, each)

        elif sel_channels:
            channels_list = if_sel_channels(sel_channels, each)

        else:
            pass

    mute_logic(channels_list)

main()
