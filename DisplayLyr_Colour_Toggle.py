import maya.cmds as mc

all_dLayers = mc.ls(type="displayLayer")
my_colours = []
chosen_colour = 17

for layer in all_dLayers:
    colour = mc.getAttr(layer + ".color")
    if colour == chosen_colour:
        my_colours.append(layer)

onOff = mc.getAttr(my_colours[0] + ".visibility")

for layer in my_colours:
    if onOff == 0:
        mc.setAttr(layer + ".visibility", 1)
        mc.layerButton(layer, edit=True, layerVisible=1)
    else:
        mc.setAttr(layer + ".visibility", 0)
        mc.layerButton(layer, edit=True, layerVisible=0)
