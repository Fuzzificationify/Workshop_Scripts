import maya.cmds as mc

sel = mc.ls(sl=1)
positions = []
pos_list = []
# Make Curve

for i, cube in enumerate(sel):
    if pos_list != []:
        positions.append(pos_list)
    pos_list = []
    for c in (sel[i:]):
        trans = mc.xform(c, q=1, ws=1, t=1)
        pos_list.append(trans)

for p in positions:

    curv1 = mc.curve(p=p, degree=3)

    motion_curv = make_nurbs(sel[-1])
    mc.attachCurve(curv1, motion_curv, replaceOriginal=1)

def make_nurbs(obj):
    positions = []

    minTime = mc.playbackOptions(q=1, minTime=1)
    maxTime = mc.playbackOptions(q=1, maxTime=1)

    for frame in range(int(minTime), int(maxTime)):
        # Get worldspace using end of .worldMatrix (last 4 values)
        valueList = mc.getAttr((obj + '.worldMatrix'), time=(frame))

        x = valueList[-4]
        y = valueList[-3]
        z = valueList[-2]
        trans = [x, y, z]

        positions.append(trans)

    motion_curv = mc.curve(p=positions)
    return motion_curv



