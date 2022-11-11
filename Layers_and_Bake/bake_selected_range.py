# Bake From Selected TimeRange  // ToDo: Rename resulting layer

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

mc.bakeResults(sel, destinationLayer=1, time=(start, end), bakeOnOverrideLayer=1)

# Delete Constraint
child_con = mc.listRelatives(sel, children=1, type='constraint')
mc.delete(child_con, constraints=1)

# Turn off override layer one frame before and after bake range
mc.setKeyframe('BakeResults.weight', time=(start-1), value=0)
mc.setKeyframe('BakeResults.weight', time=start, value=1)
mc.setKeyframe('BakeResults.weight', time=(end-1), value=1)
mc.setKeyframe('BakeResults.weight', time=end, value=0)

# Insert protective keys around bake range
mc.setKeyframe(sel, e=1, insert=1, time=((start-1), end))

# Merge Layers (With Smart Bake because new layer is on 1s)
# Use selected layer as 'base' to merge down to
mel.eval('optionVar -intValue animLayerMergeSmartBake 1')
mel.eval('animLayerMerge {{ "{0}","BakeResults" }}'.format(sel_animLayer))


# Doesn't work because it runs before baking

#pre_layer_names = mc.treeView('AnimLayerTabanimLayerEditor', q=True, ch=1)
#post_layer_names = mc.treeView('AnimLayerTabanimLayerEditor', q=True, ch=1)
#dif = set(pre_layer_names).symmetric_difference(set(post_layer_names))
#new_layer = list(dif)
