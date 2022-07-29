import maya.cmds as mc
import pymel.core as pm

sel = mc.ls(sl=1)[0]
curve_name = mc.keyframe(sel, q=1, n=1, sl=1)

key = mc.keyframe(curve_name, q=1, sl=1, indexValue=1)[0]  # Get index
keyTime = cmds.keyframe(curve_name, q=True, index=(1, key))[-1]   # Get time from index


try:
    cuv
except:
    cuv = None

if cuv == None:
   dup_cuv = mc.duplicate(curve_name, name="temp_animCurv"))
   cuv = pm.ls(dup_cuv)[0]

mc.selectKey(curve_name, index=(key, key))
time_change = keyTime - 1

if pm.nodeType(cuv) == 'animCurveTL':
    val = pm.nodetypes.AnimCurveTL.evaluate(cuv, time_change)
elif pm.nodeType(cuv) == 'animCurveTA':
    val = pm.nodetypes.AnimCurveTA.evaluate(cuv, time_change)
    val = val * 57.29577951308232     # Need to mutiply by 1 radian for some reason
elif pm.nodeType(cuv) == 'animCurveTU':
    val = pm.nodetypes.AnimCurveTU.evaluate(cuv, time_change)

mc.keyframe(animation='keys', option='over', absolute=True, timeChange=time_change, valueChange=val)
