# Toggle snap-to-whole-frames in the graphEditor

snapping = mc.animCurveEditor('graphEditor1GraphEd', q=1, snapTime=1)

if snapping == "none":
    mc.animCurveEditor('graphEditor1GraphEd', e=1, snapTime="integer")

if snapping == "integer":
    mc.animCurveEditor('graphEditor1GraphEd', e=1, snapTime="none")

