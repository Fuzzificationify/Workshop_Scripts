# Negative Share Keys

graphEditorObjects = mc.selectionConnection('graphEditor1FromOutliner', q=1, object=1)

key_range = mc.keyframe(q=1, selected=1)

# Find curve with fewest keys (within selection range)
key_num = []
for curv in graphEditorObjects:
    keys = len(mc.keyframe(curv, q=1, selected=1))
    key_num.append(keys)
    
min_val = min(key_num)
min_indx = key_num.index(min_val)


key_keyframes = mc.keyframe(graphEditorObjects[min_indx], q=1)
capped_keyframes = [x for x in key_keyframes if key_range[0] <= x <= key_range[-1]]

# Removing fewest keys curve from list to loop over
graphEditorObjects.remove(graphEditorObjects[min_indx])

for curv in graphEditorObjects:
    for key in capped_keyframes:
        mc.setKeyframe(curv, time=(key, key), insert=1) 
        
    for time in range(int(key_range[0]), int(key_range[-1])):         
        if time not in capped_keyframes:
            mc.cutKey(curv, time=(time, time))
