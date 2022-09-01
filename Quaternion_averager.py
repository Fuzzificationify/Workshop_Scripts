tor_list = OpenMaya.MSelectionList()
tor_list.add('pTorus14')
tor_obj = tor_list.getDependNode(0)
tor_xform = OpenMaya.MFnTransform(tor_obj)

tor_quat = tor_xform.rotation(asQuaternion=True)
tor_quat.normalizeIt()



quat = xform.rotation(OpenMaya.MSpace.kWorld, asQuaternion=True)
quat.normalizeIt()

wop = OpenMaya.MTransformationMatrix(xform.asMatrix())
xform.setRotation(MFntMainNode.rotation(OpenMaya.MSpace.kWorld, asQuaternion=True),OpenMaya.MSpace.kWorld)

def make_quat(obj):
    dagpath = OpenMaya.MDagPath()
    
    list = OpenMaya.MSelectionList()
    list.add(obj)
    path = list.getDagPath(0)
    #node_obj = list.getDependNode(0)
    obj_xform = OpenMaya.MFnTransform(path)
    obj_quat = obj_xform.rotation(OpenMaya.MSpace.kWorld, asQuaternion=True)
    obj_quat.normalizeIt()
    
    return obj_xform, obj_quat
    

t1_xform, t1_quat = make_quat('pTorus17')
t2_xform, t2_quat = make_quat('pTorus15')


#te1_xform, te1_quat = make_quat('pToruse')
te2_xform, te2_quat = make_quat('pTorus1P')

mid = OpenMaya.MQuaternion.slerp(t1_quat, t2_quat, 0.5)
te2_xform.setRotation(mid, OpenMaya.MSpace.kObject)

wop = t1_xform.rotation(OpenMaya.MSpace.kWorld, asQuaternion=True)
