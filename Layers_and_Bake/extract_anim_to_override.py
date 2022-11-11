# Extract base animation to new layer - Uses Selected Layer as "base"

source_aLyr = mc.treeView('AnimLayerTabanimLayerEditor', q=True, selectItem=True) or []
if not source_aLyr:
    source_aLyr = "BaseAnimation"
if type(source_aLyr) == list:
    source_aLyr = source_aLyr[0]

extract_aLyr = mc.animLayer("take_aLyr", override=1, addSelectedObjects=1, extractAnimation=source_aLyr)
mc.animLayer(source_aLyr, e=1, copyAnimation=extract_aLyr)
