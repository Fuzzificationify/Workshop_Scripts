# Move to keyframe

import maya.cmds as mc

graphEditorObjects = mc.selectionConnection('graphEditor1FromOutliner', q=1, object=1)
k = mc.findKeyframe(graphEditorObjects, which="next")
mc.currentTime(k)
