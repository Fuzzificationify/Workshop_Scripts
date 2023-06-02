def normal_key():
    sel_channels = mc.channelBox('mainChannelBox', q=1, sma=1) or []
    mc.setKeyframe(attribute=sel_channels)


def insert_key_on_graph_sel():
    curve_names = mc.keyframe(q=1, selected=1, name=1)
    current_time = mc.currentTime(q=1)
    mc.setKeyframe(curve_names, insert=1, time=current_time, adjustTangent=0)

    mc.selectKey(curve_names, time=(current_time, current_time))


if mc.keyframe(q=1, selected=1):
    insert_key_on_graph_sel()
else:
    normal_key()
