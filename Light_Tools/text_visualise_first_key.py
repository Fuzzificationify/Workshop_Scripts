def find_globals():
    dogs = pm.ls("chrWartDog*:*", type="rigMasterShapeNode")
    controls = []

    for d in dogs:
        name_space = d.namespace()
        chest_ctrl = name_space + "ctrl_m_spineIkChest"
        controls.append(chest_ctrl)

    return controls

def find_first_key(ctrl):
    times = mc.keyframe(ctrl, q=1, timeChange=1)
    first_time = int(sorted(times)[0])

    return first_time

def create_number(scale_val=200, rotate_val=170):

    controls = find_globals()

    if mc.objExists("Visual_Numbers_grp"):
        mc.delete("Visual_Numbers_grp")

    else:
        number_group = mc.group(n="Visual_Numbers_grp", empty=1, world=1)

    for ctrl in controls:
        first_key = str( find_first_key(ctrl) )
        text_obj = mc.textCurves(n='first', f='Courier', t=first_key)

        # Transform to make readable
        mc.xform(text_obj, scale=(scale_val,scale_val,scale_val) )
        mc.xform(text_obj, rotation=(0,rotate_val,0) )

        mc.pointConstraint(ctrl, text_obj, mo=0, offset=(0, 250, 0))
        mc.parent(text_obj, number_group)


create_number()
