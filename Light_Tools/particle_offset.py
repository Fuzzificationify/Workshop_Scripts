import maya.cmds as mc

weight_att = 0.1
smooth_att = 1


def get_time_info():
    min_time = mc.playbackOptions(q=1, minTime=1)
    max_time = mc.playbackOptions(q=1, maxTime=1)
    time_range = min_time, max_time

    return time_range

def get_trans_from_matrix(selection, min_time):
    sel_matrix = mc.getAttr(selection + ".worldMatrix", time=min_time-50)
    sel_trans = (sel_matrix[-4], sel_matrix[-3], sel_matrix[-2])

    return sel_trans

def make_dynamics(selection, sel_trans, weight_att):
    emitr = mc.emitter(pos=sel_trans)
    parti_tran, parti = mc.particle()
    mc.connectDynamic(parti, em=emitr)
    mc.goal(parti, goal=selection, weight=weight_att, useTransformAsGoal=1)

    return parti, parti_tran, emitr

def prime_dyno_node_attrs(parti, smooth_att, min_time):
    mc.setAttr(parti + ".maxCount", 1)
    mc.setAttr(parti + ".goalSmoothness", smooth_att)
    mc.setAttr(parti + ".startFrame", min_time-50)
    mc.playbackOptions(minTime=min_time-50)

def make_driven_loc(name_number):
    loc_name = "Dyno_Loc_" + name_number
    temp_loc = mc.spaceLocator(n=loc_name)[0]
    print(temp_loc)
    return temp_loc

def connect_loc_to_parti(loc, parti):
    mc.connectAttr(parti + ".worldCentroid", loc + ".translate")

def bake_sim(loc_list, time_range):
    mc.bakeResults(loc_list, simulation=1, time=(time_range[0]-50, time_range[1]))

def clean_up(emitr, parti_tran, min_time):
    mc.delete(emitr, parti_tran)
    mc.playbackOptions(animationStartTime=min_time)

def main():
    sel = mc.ls(sl=1)
    time_range = get_time_info()
    loc_list = []
    i = 0

    for item in sel:
        item_trans = get_trans_from_matrix(item, time_range[0])
        parti, parti_tran, emitr = make_dynamics(item, item_trans, weight_att)
        prime_dyno_node_attrs(parti, smooth_att, time_range[0])

        loc = make_driven_loc(str(i))
        connect_loc_to_parti(loc, parti)
        loc_list.append(loc)

    bake_sim(loc_list, time_range)
    clean_up(emitr, parti_tran, time_range[0])

main()

def to_animLayer():
    # Copy New Animation to Anim Layer
    mc.copyKey(temp_loc, attribute=('translate'))
    layer_name = sel + "_aLyr"
    if mc.objExists(layer_name):
        layer_name = layer_name + "1"

    mc.animLayer(layer_name)
    mc.select(sel, replace=True)
    mc.animLayer(layer_name, e=1, addSelectedObjects=1, override=1)

    mc.pasteKey(sel, animLayer=layer_name)
