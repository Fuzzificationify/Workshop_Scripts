# Merge Layer From Selected TimeRange  // ToDo: Rename resulting layer

import maya.cmds as mc
import maya.mel as mel

# Get Highlighted Time Range
aTimeSlider = mel.eval('$tmpVar=$gPlayBackSlider')
timeRange = mc.timeControl(aTimeSlider, q=True, rangeArray=True)
start, end = timeRange[0], timeRange[1]

# Check with size of range if there's no highlighted selection
if start == end-1:
    mc.confirmDialog(title="Warning", message="Make Timeslider Range Selection")
    exit()
    
sel = mc.ls(sl=1)
# Find selected animlayer
sel_animLayer = mc.treeView('AnimLayerTabanimLayerEditor', q=True, selectItem=True)[0]

# 'Bake' on 1s the frame range
for i in range(int(start), int(end)):
    mc.setKeyframe(sel, time=(i, i), insert=1)

# Find layer weights at start and end
start_weight = mc.getAttr(sel_animLayer + ".weight", time=start)
end_weight = mc.getAttr(sel_animLayer + ".weight", time=end)

# Turn off override layer one frame before and after bake range
mc.setKeyframe(sel_animLayer + '.weight', time=(start-1), value=0)
mc.setKeyframe(sel_animLayer + '.weight', time=start, value=start_weight)
mc.setKeyframe(sel_animLayer + '.weight', time=(end-1), value=end_weight)
mc.setKeyframe(sel_animLayer + '.weight', time=end, value=0)

# Insert protective keys around bake range
mc.setKeyframe(sel, e=1, insert=1, time=((start-1), end))

# Use selected layer as 'base' to merge down to
mel.eval('optionVar -intValue animLayerMergeSmartBake 1')
mel.eval('animLayerMerge {{ "BaseAnimation","{0}" }}'.format(sel_animLayer))

mc.select(sel)
