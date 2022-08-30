import maya.cmds as mc

# Script is dumb because scaleKey only works on current selection
valueScale = 0.9
anim_curvs = mc.keyframe(q=1, selected=1, name=1)
selected_keys = {}

for i, curv in enumerate(anim_curvs):
    key_sel = mc.keyframe(curv, q=1, selected=1, indexValue=1)
    selected_keys[i] = (key_sel[0], key_sel[-1])
    
for i, curv in enumerate(anim_curvs):
    previous_sel_key = selected_keys[i][0] - 1
    first_val = mc.keyframe(curv, q=1, valueChange=1)[previous_sel_key]

    # Selecting just current curve's keys for Scale to work
    mc.selectKey(curv, index=selected_keys[i])
    mc.scaleKey(valuePivot=first_val, valueScale=0.9, scaleSpecifiedKeys=1)
    
# Selecting original selection again
for i, curv in enumerate(anim_curvs):  
    mc.selectKey(curv, index=selected_keys[i], add=1)
