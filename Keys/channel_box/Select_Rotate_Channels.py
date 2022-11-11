import maya.cmds as mc

sel = mc.ls(sl=1)

appendix = ['.rx', '.ry', '.rz']
newSel = []

channels = mc.channelBox('mainChannelBox', q=1, sma=1)
        
if (channels is None) or (all(elem not in channels  for elem in ['rx', 'rz', 'ry'])):
    for ctrl in sel:
  
        for each in appendix:
        
            newSel.append(ctrl + each)
           
    mc.channelBox('mainChannelBox', edit=1, select=newSel)
    
elif len(channels) == 3:
    for ctrl in sel:
        mc.channelBox('mainChannelBox', edit=1, select=ctrl + '.rx')
        
elif 'rx' in channels:    
    for ctrl in sel:
        mc.channelBox('mainChannelBox', edit=1, select=ctrl + '.ry')
        
elif 'ry' in channels:    
    for ctrl in sel:
        mc.channelBox('mainChannelBox', edit=1, select=ctrl + '.rz')
        
elif 'rz' in channels:
        for ctrl in sel:
    
            for each in appendix:
        
                newSel.append(ctrl + each)
            
        mc.channelBox('mainChannelBox', edit=1, select=newSel)
