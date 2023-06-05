import maya.cmds as mc
import pymel.core as pm


def select_object(object):
    mc.select(object, replace=1)

def get_selected_objects():
    objects = mc.ls(sl=1)

    return objects

def mute_check(obj):
    chans = mc.listAnimatable(obj) or []
    for c in chans:
        if mc.mute(c, q=1) == True:
            return True
    else:
        return False


def mute_this(obj_attr_list):
    if mc.keyframe(obj_attr_list, q=1):
        mc.mute(obj_attr_list)
    else:
        pass

def unmute_this(obj_attr_list):
    if mc.keyframe(obj_attr_list, q=1):
        mc.mute(obj_attr_list, disable=1)
    else:
        pass

def mute_toggler(obj):
    if mute_check(obj) == False:
        print('yep')
        obj.t.mute()
    else:
        print('nope')
        obj.t.mute(disable=1)


def get_scene_mutes():
    all_mutes = mc.ls(type="mute")
    all_mute_channels = mc.listConnections(all_mutes, plugs=1, source=0, destination=1)

    return all_mute_channels

def get_scene_muted_objs():
    all_mutes = mc.ls(type="mute") or []
    if all_mutes:
        mute_objs = mc.listConnections(all_mutes, source=0, destination=1) or []
        unique_mute_objs = list(set(mute_objs)) # To remove duplicates

        all_mute_xforms = mc.ls(unique_mute_objs, type="transform")
        all_mute_joints = []
        all_mute_objs = all_mute_xforms + all_mute_joints

        return all_mute_objs
    else:
        return []

def get_attrs_from_cbox(obj):

    source_channels_list = mc.listAttr(obj, keyable=1) or []
    source_channels_list = sorted(list(set(source_channels_list)))

    translates = ["translateX", "translateY", "translateZ"]
    rotates = ["rotateX", "rotateY", "rotateZ"]

    # Seperate out common transforms so they're in a normal order
    translate_chans = [chan for chan in source_channels_list if chan in translates]
    rotate_chans = [chan for chan in source_channels_list if chan in rotates]

    other_chans = [chan for chan in source_channels_list if chan not in (translate_chans + rotate_chans)]

    return translate_chans, rotate_chans, other_chans
