# Select Constrained Object from Driver

sel = mc.ls(sl=1)
# Find connected constraint
constraints = list(set(mc.listConnections(sel, type="constraint")))

mc.select(clear=1)

for con in constraints:
    connections = []
    
    transforms = mc.listConnections(con, scn=1, type="transform", exactType=1, d=0) or []
    joints = mc.listConnections(con, scn=1, type="joint", exactType=1, d=0) or []
    if transforms: connections.extend(transforms)
    if joints: connections.extend(joints)
    
    for obj in connections:
        if obj not in sel:
            mc.select(obj, add=1)
