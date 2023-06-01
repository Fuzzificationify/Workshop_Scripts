import maya.cmds as mc
import math
import operator

from Helper_Functions import keyframe_helpers as kh

def get_direction(value, value2):
    if value >= value2:
        direction = -1

    if value <= value2:
        direction = 1

    comp = set_operator(direction)
    return comp

def set_operator(direction):
    if direction == 1:
        comp = operator.lt # Less Than
    if direction == -1:
        comp = operator.gt # Greater Than

    return comp

def value_compare_loop(anim_curve, index_list, start_idx, idx, counter, sign, comp):
    while comp(index_list[counter], index_list[counter+1]):
        final_index = mc.keyframe(anim_curve, q=1, indexValue=1)[-1]
        if idx >= final_index:
            idx = idx + 1
            break
        if idx < 0:
            # This is obviously stupid, but it counters the maths later if it's
            # looking for the first frame
            idx = -2
            break

        value = mc.keyframe(anim_curve, q=1, index=(idx,idx), valueChange=1)[0]
        index_list.append(value)

        idx = idx + sign
        counter = counter + 1

    # Adjusting values here because I cant work out how to do it in the while part
    idx = idx - int( math.copysign(2, sign) )

    mc.selectKey(clear=1)
    mc.selectKey(anim_curve, index=(start_idx,idx))

def if_equal_loop(anim_curve, index_list, start_idx, idx, counter, sign):
    print(index_list[counter])
    print(index_list[counter+1])
    while index_list[counter] == index_list[counter+1]:
        final_index = mc.keyframe(anim_curve, q=1, indexValue=1)[-1]

        if idx >= final_index:
            break
        if idx < 0:
            idx = idx + 1
            break

        value = mc.keyframe(anim_curve, q=1, index=(idx, idx), valueChange=1)[0]
        index_list.append(value)

        idx = idx + sign
        counter = counter + 1

    mc.selectKey(clear=1)
    mc.selectKey(anim_curve, index=(start_idx, idx))

def save_key_selection():
    anim_curve = mc.keyframe(q=1, n=1)
    indices = mc.keyframe(q=1, s=1, indexValue=1)

    return anim_curve, indices

def reselect_keys(anim_curve, indices):
    mc.selectKey(anim_curve, index=(indices[0], indices[-1]), add=1)

def get_sign(sign):
    if sign == "positive":
        sign = 1
        i = -1 # For getting the last value of list
    if sign == "negative":
        sign = -1
        i = 0 # For getting first value of list

    return sign, i

def main(sign="positive"):
    print("RUNNING")
    # If no selection, select neighbour key in the correct direction
    if not mc.keyframe(q=1, sl=1, n=1):
        if sign == "positive":
            neighbour = "next"
        if sign == "negative":
            neighbour = "previous"
        kh.select_neighbour_key(neighbour)

    index_list = []
    counter = 0
    sign, i = get_sign(sign)

    anim_curve, indices = save_key_selection()

    idx = mc.keyframe(anim_curve, q=1, selected=1, indexValue=1)[i]
    start_idx = idx

    value = mc.keyframe(anim_curve, q=1, index=(idx, idx), valueChange=1)[0]
    value2 = mc.keyframe(anim_curve, q=1, index=(idx + sign, idx + sign), valueChange=1)[0]

    index_list.append(value)
    index_list.append(value2)

    idx = idx + int(math.copysign(2, sign))  # Use copysign to add 2 or minus 2

    if value == value2:
        if_equal_loop(anim_curve, index_list, start_idx, idx, counter, sign)
        pass

    else:
        comp = get_direction(value, value2)
        value_compare_loop(anim_curve, index_list, start_idx, idx, counter, sign, comp)

    reselect_keys(anim_curve, indices)
