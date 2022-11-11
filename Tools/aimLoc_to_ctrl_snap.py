import maya.cmds as mc

ctrls = mc.ls(sl=1)

locs = mc.ls(sl=1)

minTime = mc.playbackOptions(q=1, minTime=1)
maxTime = mc.playbackOptions(q=1, maxTime=1)

for frame in range(int(minTime), int(maxTime)):

    for i, ctrl in enumerate(ctrls):
        #ctrl_pos = mc.getAttr(ctrl + '.t')[0]
        #mc.setAttr(locs[i] + '.t', ctrl_pos[0], ctrl_pos[1], ctrl_pos[2])
    
        valueList = mc.getAttr(ctrl+'.worldMatrix', time=(frame))

        x = valueList[-4]
        y = valueList[-3]
        z = valueList[-2]
        trans = [x, y, z]
    
        if i>1:
            
            mc.setKeyframe(locs[i-1] + '.translateX', value = trans[0], time = frame)
            mc.setKeyframe(locs[i-1] + '.translateY', value = trans[1], time = frame)
            mc.setKeyframe(locs[i-1] + '.translateZ', value = trans[2], time = frame)


##############################

# Single / Selective
def loc_to_ctrl_snap(ctrls, locs):
    minTime = mc.playbackOptions(q=1, minTime=1)
    maxTime = mc.playbackOptions(q=1, maxTime=1)
    print('wop')
    for frame in range(int(minTime), int(maxTime)):
        print('yoop')
        for i, ctrl in enumerate(ctrls):
            valueList = mc.getAttr(ctrl+'.worldMatrix', time=(frame))

            x = valueList[-4]
            y = valueList[-3]
            z = valueList[-2]
            trans = [x, y, z]
        

            print('yep')
            mc.setKeyframe(locs[i] + '.translateX', value = trans[0], time = frame)
            mc.setKeyframe(locs[i] + '.translateY', value = trans[1], time = frame)
            mc.setKeyframe(locs[i] + '.translateZ', value = trans[2], time = frame)
                
                
loc_to_ctrl_snap(ctrls, locs)
