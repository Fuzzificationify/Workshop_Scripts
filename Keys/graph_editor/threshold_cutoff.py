# Threshold cutoff

import maya.cmds as mc
import math

def get_curve_direction(anim_curve):
    values = (mc.keyframe(anim_curve, q=1, selected=1, valueChange=1))
    start_key_val = values[0]
    following_sum = sum(values[1:])
    following_avg = following_sum / len(values[1:])

    if start_key_val >= following_avg:
        curve_direction = -1
        peak = 0
        return curve_direction, peak
    if start_key_val <= following_avg:
        curve_direction = 1
        peak = -1   # -1 means the last item of the sorted values
        return curve_direction, peak


def main():
    sel = mc.ls(sl=1)
    anim_curve = mc.keyframe(sel, q=1, selected=1, name=1)[0]
    keyframes = mc.keyframe(sel, q=1, selected=1, indexValue=1)

    curv_direction, peak = get_curve_direction(anim_curve)

    values = sorted(mc.keyframe(sel, q=1, selected=1, valueChange=1))
    peak_val = (values[peak])                  # Get either greatest or lowest value
    range_val = math.copysign((values[0] - values[-1]), curv_direction)   # Get range between first and last keys

    cut_off_val = peak_val - (range_val / 10)


    for i in keyframes:
        i_val = mc.keyframe(anim_curve, q=1, index=(i, i), valueChange=1)[0]
        print(i_val)

        if curv_direction == -1:
            if i_val < cut_off_val:
                mc.keyframe(anim_curve, e=1, index=(i, i), valueChange=cut_off_val)

        if curv_direction == 1:
            if i_val > cut_off_val:
                mc.keyframe(anim_curve, e=1, index=(i, i), valueChange=cut_off_val)


main()
