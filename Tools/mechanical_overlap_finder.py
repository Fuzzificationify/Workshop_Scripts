import maya.cmds as mc
import locator_creations

source_obj, offset_obj = mc.ls(sl=1)

temp_loc = locator_creations.baked_loc(source_obj)

all_anim_attrs = mc.listAnimatable(temp_loc)
delta_list = []

for attr in all_anim_attrs:
    if 'translate' in attr:

        numKeyframes = mc.keyframe(attr, q=True, keyframeCount=True)
        
        keys = mc.keyframe(attr, q=1, index=(0, numKeyframes), valueChange=1)
        times = mc.keyframe(attr, q=1, index=(0, numKeyframes), timeChange=1)

        for i, val in enumerate(keys):
            if i < (len(keys)-1):
                delta = keys[(i + 1)] - keys[i]
                #fliping values
                delta = delta * -1
                key_time = times[i]
                delta_list.append((delta, key_time))

        just_attr = attr.split('.')[-1]
        #Set Keys
        offset_obj_xform = mc.getAttr(offset_obj + '.' + just_attr)
        for j in range(len(delta_list)):
            mc.setKeyframe(offset_obj + '.' + just_attr, value=(offset_obj_xform + delta_list[j][0]), time=delta_list[j][1])

mc.delete(temp_loc)
