# Select Material from Selection
# Note: If Selection has more than one material, they won't both appear in Attribute Editor

sel = mc.ls(sl=1)
sel_shape = mc.listRelatives(sel, children=1, shapes=1)[0]

shading_grp = mc.listConnections(sel_shape, source=0, destination=1, type='shadingEngine')
if len(shading_grp) > 1:
    print("More than one!!")

mc.select(clear=1)

for each_shr in shading_grp:
    shader = mc.listConnections(each_shr + '.surfaceShader', source=1, destination=0)
    mc.select(shader, add=1)
