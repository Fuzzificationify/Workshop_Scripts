# Refresh Channel Selection

channels = mc.channelBox('mainChannelBox', q=1, sma=1)

sel = mc.ls(sl=1)
objs_chans_list = []

for obj in sel:
    for chan in channels:
        objs_chans_list.append(obj + '.' + chan)

mc.channelBox('mainChannelBox', edit=1, select=objs_chans_list)
