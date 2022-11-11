# Offset Animation
# Top Tip: Use can use the attribute rather than the animCurve, then the animLayer stuff should be taken care of for you. 
#          E.g. Use mc.keyframe('Sphere1.tx', timeChange=5), rather than mc.keyframe('pSphere1_translateY_AnimLayer2_inputB', timeChange=5)
#          Find the attributes from GraphEditor with mc.selectionConnection('graphEditor1FromOutliner', q=1, object=1) 

#          You can also use mc.keyframe on the object without an attribute, 
#          e.g. mc.keyframe('pSphere1', q=1) and it will return values for all animCurves on the selected Animlayer

import maya.cmds as mc

ctrl_list = mc.ls(sl=1)
exception_list = []

start_frame = 30

i = 0
offset = 2

for ctrl in ctrl_list:
    last_frame = mc.keyframe(ctrl, q=1)[-1]
    if start_frame != 0:
        mc.keyframe(ctrl, edit=1, time=(start_frame,last_frame), relative=1, timeChange=i)
    else:
        mc.keyframe(ctrl, edit=1, relative=1, timeChange=i)
    
    if ctrl not in exception_list:
        i = i + offset

         




# With mid_point

import maya.cmds as mc

ctrl_list = mc.ls(sl=1)
exception_list = []

start_frame = 0

i = 0
offset = 3
mid_point = (offset * 5)
hit = 0

for ctrl in ctrl_list:
    animCurve = mc.listConnections(ctrl, t="animCurve")
    last_frame = mc.keyframe(animCurve, q=1)[-1]
    if start_frame != 0:
        mc.keyframe(animCurve, edit=1, time=(start_frame,last_frame), relative=1, timeChange=i)
    else:
        mc.keyframe(animCurve, edit=1, relative=1, timeChange=i)
    
    if ctrl not in exception_list:
        if i >= mid_point or (hit==1):
            hit = 1
            i = i - (offset * 0.75)
        else:
            i = i + offset



###########################

# Old
import maya.cmds as mc

ctrl_list = mc.ls(sl=1)
exception_list = []

start_frame = 30

i = 0
offset = 2

for ctrl in ctrl_list:
    animCurve = mc.listConnections(ctrl, t="animCurve")
    last_frame = mc.keyframe(animCurve, q=1)[-1]
    if start_frame != 0:
        mc.keyframe(animCurve, edit=1, time=(start_frame,last_frame), relative=1, timeChange=i)
    else:
        mc.keyframe(animCurve, edit=1, relative=1, timeChange=i)
    
    if ctrl not in exception_list:
        i = i + offset

