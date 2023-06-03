# Make Simple Locator - ;

import maya.cmds as mc
import pymel.core as pm
import timeit
import maya.utils
import Helper_Functions.keyframe_helpers as kh


class UndoContext(object):
    def __enter__(self):
        mc.undoInfo(openChunk=True)
    def __exit__(self, *exc_info):
        mc.undoInfo(closeChunk=True)


def get_frame_range(obj):
    all_keys = sorted(mc.keyframe(obj, q=1) or [])
    if all_keys != []:
        start_end_keys = all_keys[0], all_keys[-1]
    else:
        start_end_keys = []

    return start_end_keys

def smart_frame_range(sel):
    if len(sel) > 1:
        start_end_keys = kh.get_scene_range()
    else:
        # Get frame range from obj's keys
        start_end_keys = get_frame_range(sel[0])

    return start_end_keys

def make_clean_loc(obj, suffix="_loc"):
    obj_nn = obj.rpartition(":")[2]
    loc = mc.spaceLocator(n=obj_nn + suffix)[0]
    loc = mc.ls(loc, long=1) # Long name

    custom_attr_base(loc)

    return loc[0] # Returns loc not list


def find_parent_and_parent(obj, loc):
    # loc is long name, so because I reparent it, I'm using short name here
    # So I get new loc name when parenting, and find new long name from that

    parent_node = mc.pickWalk(obj, d="up")[0]
    # Parent unless it's parent is world
    if parent_node != obj:
        parented_loc = mc.parent(loc, parent_node, relative=1)
    loc_new_long = mc.ls(parented_loc, l=1)[0]

    # Copy Attrs
    mc.copyAttr(obj, loc_new_long, values=1)

    return loc_new_long

def find_unkeyable_channels(obj):
    channel_list = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz']
    skip_rot = []
    skip_tran = []

    for chan in channel_list:
        # Skip channels marked unkeyable
        if mc.getAttr(obj + "." + chan, k=1) == False:
            if chan[0] == 't':
                skip_tran.append(chan[1])
            if chan[0] == 'r':
                skip_rot.append(chan[1])

    return skip_rot, skip_tran


def append_unkeyable_channels(obj, skip_rot, skip_tran):
    channel_list = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz']

    for chan in channel_list:
        # Skip channels marked unkeyable
        if mc.getAttr(obj + "." + chan, k=1) == False:
            if chan[0] == 't':
                skip_tran.append(chan[1])
            if chan[0] == 'r':
                skip_rot.append(chan[1])

    return skip_rot, skip_tran


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

    # #remove dups
    # skip_rot = list( set(skip_rot) )
    # skip_tran = list( set(skip_tran) )

    return (skip_rot, skip_tran, sel_channels)


def custom_attr_base(loc_list):
    for l in (loc_list):
        loc = pm.ls(l)[0]
        # Make J_loc attr to mark it as mine
        loc.addAttr('j_loc', at='enum', enumName="          ")
        loc.j_loc.set(channelBox=1)

        set_custom_outliner_colour(loc, colour="Base")

def custom_attr_constrained(loc):
    set_custom_outliner_colour(loc, colour="Constrained")


def custom_attr_controller(loc_list, obj_list):
    # Custom Attr is called "master"
    for l, obj in zip(loc_list, obj_list):
        loc = pm.ls(l)[0]
        loc.addAttr('master', dataType='string')

        # Set obj name as .master attr
        loc.master.set(obj, type='string')

        # Set custom colour to show it has attribute
        set_custom_outliner_colour(loc, colour="Controller")


def get_custom_locs():
    locs = pm.ls(type="locator")

    for loc in locs:
        xform_loc = loc.getParent()
        if xform_loc.hasAttr('master'):
            print(xform_loc + " yup")

def set_custom_outliner_colour(loc, colour="Base"):
    if colour == "Base": r, g, b = 0.8, 0.5, 0.3
    if colour == "Constrained": r, g, b = 0.7, 0.85, 1
    if colour == "Controller": r, g, b = 0, 1, 0.2

    mc.setAttr(loc + ".useOutlinerColor", 1)
    mc.setAttr(loc + ".outlinerColor", r, g, b)

####################################################################################################
####################################################################################################


def simple_loc(selection):

    if selection:
        for obj in selection:

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
def constrained_loc(selection):
    if selection:
        loc_list = []
        constraint_list = []

        for obj in selection:

            # Remove namespace, make loc
            loc = make_clean_loc(obj)

            # Setup for constrained-type J locator
            custom_attr_constrained(loc)

            # Use selection's rotateOrder
            ro = mc.getAttr(obj + ".rotateOrder")
            mc.setAttr(loc + ".rotateOrder", ro)

            # Compare selected channels to list and append 'skipped' items to relevant list
            skip_rot, skip_tran = find_channels_to_skip()[:2]

            con = mc.parentConstraint(obj, loc, skipRotate=skip_rot, skipTranslate=skip_tran)[0]

            loc_list.append(loc)
            constraint_list.append(con)
    else:
        pass

    return loc_list, constraint_list

# Locator as Controller - Ctrl + Shift + l
def controller_loc(selection):
    # Convert argument to list if single item
    if type(selection) != list:
        sel = [selection]
    else:
        sel = selection

    with UndoContext():
        mc.evalDeferred(lambda: controller_loc_setup(selection))

def controller_loc_setup(sel):
    loc_ctrlr_list = []
    constraint_list = []

    if sel:

        # Compare selected channels to list and append 'skipped' items to relevant list
        skip_rot, skip_tran, sel_channels = find_channels_to_skip()

        start_end_keys = smart_frame_range(sel)

        for obj in sel:
            # Remove namespace, make loc
            loc = make_clean_loc(obj)

            # Use selection's rotateOrder
            ro = mc.getAttr(obj + ".rotateOrder")
            mc.setAttr(loc + ".rotateOrder", ro)

            loc_ctrlr_list.append(loc)

            # Append unkeyable channels to skip lists
            skip_rot, skip_tran = append_unkeyable_channels(obj, skip_rot, skip_tran)

            pCon = mc.parentConstraint(obj, loc, skipRotate=skip_rot, skipTranslate=skip_tran)[0]
            constraint_list.append(pCon)

        # Deferring because when animlayer is present, a constraint followed by baking causes a dramatic slow-down
        bake_args = [loc_ctrlr_list, start_end_keys, sel_channels]
        reconstrain_args = [constraint_list, sel, loc_ctrlr_list, skip_rot, skip_tran]
        custom_attr_controller_args = [loc_ctrlr_list, sel]

        make_controller(bake_args, reconstrain_args, custom_attr_controller_args)
        # mc.evalDeferred(lambda: just_bake(loc_ctrlr_list, start_end_keys, sel_channels))
        # mc.evalDeferred(lambda: reconstrain(constraint_list, sel, loc_ctrlr_list, skip_rot, skip_tran))
        # mc.evalDeferred(lambda: custom_attr_controller(loc_ctrlr_list, sel))


    return loc_ctrlr_list

def make_controller(bake_args, reconstrain_args, custom_attr_controller_args):
    loc_ctrlr_list, start_end_keys, sel_channels = bake_args
    mc.evalDeferred(lambda: just_bake(loc_ctrlr_list, start_end_keys, sel_channels))

    constraint_list, sel, loc_ctrlr_list, skip_rot, skip_tran = reconstrain_args
    mc.evalDeferred(lambda: reconstrain(constraint_list, sel, loc_ctrlr_list, skip_rot, skip_tran))

    loc_ctrlr_list, sel = custom_attr_controller_args
    mc.evalDeferred(lambda: custom_attr_controller(loc_ctrlr_list, sel))


def just_bake(obj, start_end_keys, channels):
    print('running bake')
    mc.bakeResults(obj, time=start_end_keys, attribute=channels)

def reconstrain(pCons, obj_list, loc_list, skip_rot, skip_tran):
    print('running reconstrain')
    mc.delete(pCons)
    for obj, loc in zip(obj_list, loc_list):
        mc.parentConstraint(loc, obj, w=1, skipRotate=skip_rot, skipTranslate=skip_tran)


# Baked Loc - no controlling constraint
def baked_loc(selection):
        # Convert argument to list if single item
    if type(selection) != list:
        sel = [selection]
    else:
        sel = selection
    loc_ctrlr_list = []

    if sel:

        # Compare selected channels to list and append 'skipped' items to relevant list
        skip_rot, skip_tran, sel_channels = find_channels_to_skip()

        for obj in sel:
            # Get frame range from obj's keys
            start_end_keys = get_frame_range(obj)

            # Remove namespace, make loc
            loc = make_clean_loc(obj)

            # Use selection's rotateOrder
            ro = mc.getAttr(obj + ".rotateOrder")
            mc.setAttr(loc + ".rotateOrder", ro)

            # Append unkeyable channels to skip lists
            skip_rot, skip_tran = append_unkeyable_channels(obj, skip_rot, skip_tran)

            pCon = mc.parentConstraint(obj, loc, skipRotate=skip_rot, skipTranslate=skip_tran)

            # Bake Controller Loc
            if start_end_keys != []:
                mc.bakeResults(loc, time=start_end_keys, attribute=sel_channels)
            mc.delete(pCon)
    
            loc_ctrlr_list.append(loc)
    return loc_ctrlr_list


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

        # Compare selected channels to list and append 'skipped' items to relevant list
        skip_rot, skip_tran = find_channels_to_skip()[:2]

        for obj in sel:
            # Get frame range from obj's keys
            start_end_keys = get_frame_range(obj)

            # Remove namespace, make loc
            loc = make_clean_loc(obj)

            # Put loc in parent of sel's space and copy attributes
            loc = find_parent_and_parent(obj, loc)

            # Append unkeyable channels to skip lists
            skip_rot, skip_tran = append_unkeyable_channels(obj, skip_rot, skip_tran)

            #pCon = mc.parentConstraint(obj, loc, skipRotate=skip_rot, skipTranslate=skip_tran)
            pCon = mc.parentConstraint(obj, loc)

            # Bake Controller Loc
            mc.bakeResults(loc, time=start_end_keys)
            mc.delete(pCon)

            pCon2 = mc.parentConstraint(loc, obj, w=1, skipRotate=skip_rot, skipTranslate=skip_tran)
            mc.select(loc)


def controller_in_sel_space(source, space_obj):
    print('{}{}'.format('source:', source))
    loc_list, con_list = constrained_loc(source)
    print('{}{}'.format('con_list: ', con_list))

    loc_list_2 = []
    for loc in loc_list:
        loc = mc.parent(loc, space_obj)[0]
        loc_list_2.append(loc)

    skip_rot, skip_tran, sel_channels = find_channels_to_skip()
    start_end_keys = smart_frame_range(source)

    bake_args = [loc_list_2, start_end_keys, sel_channels]
    reconstrain_args = [con_list, source, loc_list_2, skip_rot, skip_tran]
    custom_attr_controller_args = [loc_list_2, source]

    make_controller(bake_args, reconstrain_args, custom_attr_controller_args)


    pass



def testBake():
    ctrl = ['chrGiantOctopus01A_13009_0:ctrl_l_tentacleCFwdIkFkFkF']
    loc = 'ctrl_l_tentacleCFwdIkFkFkF_loc'
    start_end_keys = (1, 120)
    t1_start = timeit.default_timer()

    for obj in ctrl:

        print('obj', obj)

        pCon = mc.parentConstraint(obj, loc)


        pre_bake_time = timeit.default_timer() - t1_start
        print('{}:{}'.format('pre_bake_time', pre_bake_time))

        # Bake Controller Loc
        if start_end_keys != []:
            mc.evalDeferred(lambda: mc.bakeResults(loc, time=start_end_keys))
            #mc.bakeResults(loc, time=start_end_key)

        post_bake_time = timeit.default_timer() - t1_start
        print('{}:{}'.format('post_bake_time', post_bake_time))


    end_time = timeit.default_timer() - t1_start
    print('{}:{}'.format('end_time', end_time))

