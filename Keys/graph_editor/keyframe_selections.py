# Keyframe Selections 
import maya.cmds as mc

def step_through_keys(expand=0, direction="back", subtract=0):

    # If no selection, select next key frame 
    if check_sel(direction):
        return

    selKey_options = {'add' : 1, 'remove' : 0}
    anim_curv = mc.keyframe(q=1, name=1) or []

    all_keys = sorted(mc.keyframe(anim_curv, q=1, timeChange=1))
    start_key, end_key = int(all_keys[0]), int(all_keys[-1])

    min_sel_key = int(sorted(mc.keyframe(anim_curv, q=1, selected=1, timeChange=1))[0])
    max_sel_key = int(sorted(mc.keyframe(anim_curv, q=1, selected=1, timeChange=1))[-1])

    if direction == "back":
        lower_bound = min_sel_key - 1
        upper_bound = start_key - 1
        stride = -1
        trailing_key = -1
        pos = -1
        
        if subtract == 1:
            upper_bound = max_sel_key
            lower_bound = lower_bound + 1
    
    
    elif direction == "forward":
        lower_bound = max_sel_key + 1
        upper_bound = end_key + 1
        stride = 1
        trailing_key = 0
        pos = 0
        
        if subtract == 1:
            upper_bound = start_key
            lower_bound = lower_bound - 1
            
    
    if subtract == 1:
        expand = 0
        stride = stride * - 1
        selKey_options = {'add' : 0, 'remove' : 1}
        
    
    for i in range(lower_bound, upper_bound, stride):
        hit_frame = mc.keyframe(anim_curv, q=1, time=(i, i+0.99))
        # Target keys between i and i.99
        if hit_frame:
            frame = hit_frame[0]
            mc.selectKey(anim_curv, time=(frame, frame), **selKey_options)
            
            # Deselect current key if successfully selected next one
            if expand == 0 and subtract == 0:
                deselect_key(anim_curv, trailing_key)
            break
     
    
def deselect_key(anim_curv, trailing_key):

    for curv in anim_curv:
        sel_keys = mc.keyframe(curv, q=1, selected=1, indexValue=1)
        if len(sel_keys) > 1:
            mc.selectKey(curv, remove=1, keyframe=1, index=(sel_keys[trailing_key],sel_keys[trailing_key]))


def check_sel(direction):
    if direction == "back":
        finder = "previous"
    if direction == "forward":
        finder = "next"
        
    selected = mc.keyframe(q=1, selected=1) or []

    if not selected:
        current_key = mc.currentTime(q=1)
        graphEditorObjects = mc.selectionConnection('graphEditor1FromOutliner', q=1, object=1)
        
        k = mc.findKeyframe(graphEditorObjects, which=finder)
        mc.selectKey(graphEditorObjects, time=(k,k))
        
        return 1
