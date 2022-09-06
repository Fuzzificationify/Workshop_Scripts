import maya.cmds as mc

def get_average_rot(rings):
    ring_rot = [mc.xform(r, q=1, ws=1, rotation=1) for r in rings]

    avg_rot = []

    for r1, r2 in zip(ring_rot[0], ring_rot[1]):
        avg = (r1 + r2) / 2
        avg_rot.append(avg)

    return avg_rot



def get_leading_vec(rings):
    # Get the positions of first and last ctrls; subtract to find vector
    ring_vec = [mc.xform(r, q=1, ws=1, translation=1) for r in rings]
    vec = []
    for t1, t3 in zip(ring_vec[0], ring_vec[-1]):
        vecc = (t1 - t3)
        vec.append(vecc)
    return vec


def aim_node(target_pos, aim_vect=[0, 1, 0], up_vect=[0, 1, 0]):
    '''aim supplied object at supplied world space position
    @param obj_to_align -- maya transform node
    @param target pos -- [x,y,z] world position to aim at
    @optional param  aim_vect -- local axis to aim at the target position
    @optional param  up_vect -- secondary axis aim vector
     '''

    cubey = mc.polyCube()
    tgt = mc.createNode('transform')  # looks like locator version doesn't work on maya 2012+
    mc.xform(tgt, t=target_pos, a=True)
    mc.select(tgt, cubey)
    const = mc.aimConstraint(aim=aim_vect, worldUpVector=up_vect, worldUpType="vector")
    mc.delete(const, tgt)

    rotate_vec = mc.xform(cubey, q=1, ws=1, rotation=1)
    mc.delete(cubey)
    return rotate_vec

def main():
    rings = mc.ls(sl=1)
    avg_rot = get_average_rot(rings)

    vec = get_leading_vec(rings)
    rotate_vec = aim_node(vec)

    fix_axis = 1
    mc.xform('pCube1', ws=1, rotation=rotate_vec)

    split_rot = [(r/2) for r in rotate_vec]

    # mc.xform(rings[0], ws=1, rotation=split_rot)
    # mc.xform(rings[1], ws=1, rotation=split_rot)

    mc.setAttr(rings[0] + '.rotateY', split_rot[1])
    mc.setAttr(rings[1] + '.rotateY', split_rot[1])
    mc.setAttr(rings[0] + '.rotateZ', split_rot[2])
    mc.setAttr(rings[1] + '.rotateZ', split_rot[2])

for 
main()
