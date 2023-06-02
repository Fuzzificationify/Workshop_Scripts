# Remove selected channels from selected AnimLayer
import maya.mel as mel

obj_sel = mc.ls(sl=1)

# Get animLayer and check one is selected
animLayer_sel = mc.treeView("AnimLayerTabanimLayerEditor", q=1, selectItem=1)[0]
if animLayer_sel == None:
    mc.confirmDialog(title=" ", message="Need AnimLayer Selection", button="Ok")

# Get selected channels
channels = mel.eval('selectedChannelBoxAttributes;')

# Combine object with channel attrs
full_attr_list = []
for obj in obj_sel:
    attrs = [obj + "." + x for x in channels]
    full_attr_list.extend(attrs)


for attr in full_attr_list:
    mc.animLayer(animLayer_sel, e=1, removeAttribute=attr)
