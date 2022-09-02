def make_quat(obj):
    list = OpenMaya.MSelectionList()
    list.add(obj)
    #node_obj = list.getDependNode(0)
    dag = list.getDagPath(0)
    obj_dag = OpenMaya.MFnTransform(dag)
    obj_quat = obj_dag.rotation(OpenMaya.MSpace.kWorld, asQuaternion=True)
    obj_quat.normalizeIt()

    return (obj_dag, obj_quat)

def find_average_rot(obj_quat_1, obj_quat_2):
    mid = OpenMaya.MQuaternion.slerp(obj_quat_1, obj_quat_2, 0.5)

    return mid


def main():
    sel = mc.ls(sl=1)
    dag_dic = {}
    dag_list = []
    dag_quat_list = []
    extra_mid_rot_list = []
    i = 0
    j = 0
    # Make dic of items in sel
    for obj in sel:
        dag_obj, dag_quat = make_quat(obj)
        dag_list.append(dag_obj)
        dag_quat_list.append(dag_quat)

    print("dag_list:", dag_list)

    # Extra ring mid rots
    for previous, current in zip(dag_quat_list, dag_quat_list[1:]):
        extra_mid = find_average_rot(previous, current)
        extra_mid_rot_list.append(extra_mid)

        cube = mc.polyCube()
        dag_c, _ = make_quat(cube)
        con = mc.pointConstraint(dag_list[j], dag_list[j+1], cube)
        dag_c.setRotation(extra_mid, OpenMaya.MSpace.kWorld)

        j = j + 1

    # Avg between the extras, and paste it onto controls
    for previous, current in zip(extra_mid_rot_list, extra_mid_rot_list[1:]):
        avg_mid = find_average_rot(previous, current)

        dag_list[i+1].setRotation(avg_mid, OpenMaya.MSpace.kWorld)
        i = i + 1
