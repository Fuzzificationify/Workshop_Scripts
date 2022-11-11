# Select Graph Editor Keys on Current Frame

time = mc.currentTime(q=1)

#Get GraphEditor Outliner Channel Selection
graphEditorObjects = mc.selectionConnection('graphEditor1FromOutliner', q=1, object=1)

mc.selectKey(clear=1)
mc.selectKey(graphEditorObjects, replace=1, time=(time,))



# Deselect Current Key
time = mc.currentTime(q=1)

#Get GraphEditor Outliner Channel Selection
graphEditorObjects = mc.selectionConnection('graphEditor1FromOutliner', q=1, object=1)

mc.selectKey(graphEditorObjects, remove=1, time=(time,))
