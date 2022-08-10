# Make Simple Locator - ;

import maya.cmds as mc


def get_frame_range(obj):
    all_keys = sorted(mc.keyframe(obj, q=1) or [])
    if all_keys != []:
        start_end_keys = all_keys[0], all_keys[-1]
    else:
        start_end_keys = []

    return start_end_keys


def make_clean_loc(obj, suffix="_loc"):
    obj_nn = obj.rpartition(":")[2]
    loc = mc.spaceLocator(n=obj_nn + suffix)[0]

    return loc


def find_parent_and_parent(obj, loc):

    parent_node = mc.pickWalk(obj, d="up")[0]
    # Parent unless it's parent is world
    if parent_node != obj:
        mc.parent(loc, parent_node, relative=1)

    # Copy Attrs
    mc.copyAttr(obj, loc, values=1)


def find_channels_to_skip(channels_list = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz']):
    # Compare selected channels to list and append 'skipped' items to relevant list
    sel_channels = mc.channelBox('mainChannelBox', q=1, sma=1)
    skip_rot = []
    skip_tran = []

    if sel_channels:
        for channel in channels_list:
            if channel not in sel_channels:
                if channel[0] == 't':
                    skip_tran.append(channel[1])
                if channel[0] == 'r':
                    skip_rot.append(channel[1])

    return (skip_rot, skip_tran, sel_channels)



####################################################################################################
####################################################################################################


def simple_loc():
    sel = mc.ls(sl=1)

    if sel:
        for obj in sel:

            # Remove namespace, make loc
            loc = make_clean_loc(obj)

            # Use selection's rotateOrder
            ro = mc.getAttr(obj + ".rotateOrder")
            mc.setAttr(loc + ".rotateOrder", ro)

            # Copy worldspace position
            transforms = mc.xform(obj, q=1, ws=1, m=1)
            mc.xform(loc, ws=1, m=transforms)

            mc.select(loc)

    else:
        mc.spaceLocator(n="my_loc1")
        mc.select(clear=True)



# Constrainted Locators - Ctrl + l

def constrained_loc():
    sel = mc.ls(sl=1)

    if sel:
        for obj in sel:

            # Remove namespace, make loc
            loc = make_clean_loc(obj)

            # Use selection's rotateOrder
            ro = mc.getAttr(obj + ".rotateOrder")
            mc.setAttr(loc + ".rotateOrder", ro)

            # Compare selected channels to list and append 'skipped' items to relevant list
            skip_rot, skip_tran = find_channels_to_skip()[:2]

            mc.parentConstraint(obj, loc, skipRotate=skip_rot, skipTranslate=skip_tran)

    else:
        pass


# Locator as Controller - Ctrl + Shift + l

def controller_loc():
    sel = mc.ls(sl=1)

    if sel:
        for obj in sel:
            # Get frame range from obj's keys
            start_end_keys = get_frame_range(obj)

            # Remove namespace, make loc
            loc = make_clean_loc(obj)

            # Use selection's rotateOrder
            ro = mc.getAttr(obj + ".rotateOrder")
            mc.setAttr(loc + ".rotateOrder", ro)

            # Compare selected channels to list and append 'skipped' items to relevant list
            skip_rot, skip_tran, sel_channels = find_channels_to_skip()

            pCon = mc.parentConstraint(obj, loc, skipRotate=skip_rot, skipTranslate=skip_tran)

            # Bake Controller Loc
            if start_end_keys != []:
                mc.bakeResults(loc, time=start_end_keys, attribute=sel_channels)
            mc.delete(pCon)

            pCon2 = mc.parentConstraint(loc, obj, w=1, skipRotate=skip_rot, skipTranslate=skip_tran)



# Locator as Local Child - Win + l

def childed_loc():
    sel = mc.ls(sl=1)

    if sel:
        for obj in sel:

            # Remove namespace, make loc
            loc = make_clean_loc(obj)

            # Use selection's rotateOrder
            ro = mc.getAttr(obj + ".rotateOrder")
            mc.setAttr(loc + ".rotateOrder", ro)

            # Put loc in parent of sel's space and copy attributes
            find_parent_and_parent(obj, loc)



# Locator as Local Controller - Win + Shift + l

def controller_childed_loc():
    sel = mc.ls(sl=1)

    if sel:
        for obj in sel:
            # Get frame range from obj's keys
            start_end_keys = get_frame_range(obj)

            # Remove namespace, make loc
            loc = make_clean_loc(obj)

            # Put loc in parent of sel's space and copy attributes
            find_parent_and_parent(obj, loc)

            # Compare selected channels to list and append 'skipped' items to relevant list
            skip_rot, skip_tran = find_channels_to_skip()[:2]

            #pCon = mc.parentConstraint(obj, loc, skipRotate=skip_rot, skipTranslate=skip_tran)
            pCon = mc.parentConstraint(obj, loc)

            # Bake Controller Loc
            mc.bakeResults(loc, time=start_end_keys)
            mc.delete(pCon)

            pCon2 = mc.parentConstraint(loc, obj, w=1, skipRotate=skip_rot, skipTranslate=skip_tran)
            mc.select(loc)
