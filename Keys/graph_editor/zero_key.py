# Keyframe Tweaker - relative to amplitude of whole animcurve

multiplier = 20.0
sign = -1.0

anim_curv = mc.keyframe(q=1, name=1, selected=1)

curv_values = sorted(mc.keyframe(anim_curv, q=1, valueChange=1))
min_val, max_val = curv_values[0], curv_values[-1]

val_dif = max_val - min_val
move_factor = sign*(val_dif / multiplier)

mc.keyframe(e=1, relative=1, valueChange=move_factor)
