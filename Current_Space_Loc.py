import maya.cmds as mc


def locTool():
    selObj = mc.ls(sl=1)

    locCtrl = LocatorOnDemand(selObj)
    ReverseConstraint(selObj, locCtrl)


def LocatorOnDemand(selObj):
    # Make a locator at selected's position
    locParent = mc.spaceLocator(n=selObj[0] + "_Loc_newSpace")

    parentCon = mc.parentConstraint(selObj, locParent)
    mc.delete(parentCon)

    # Make Child
    locCtrl = mc.spaceLocator(n=selObj[0] + "_Loc_locCtrl", p=[0, 0, 0])
    mc.parent(locCtrl, locParent)
    mc.ResetTransformations(locCtrl)

    return locCtrl


def ReverseConstraint(selObj, locCtrl):
    # Matching existing anim
    parentCon = mc.parentConstraint(selObj, locCtrl)
    myBake(selObj, locCtrl)
    mc.delete(parentCon)

    # New power constraint
    newParentCon = mc.parentConstraint(locCtrl, selObj)


def myBake(selObj, bakeObj):
    # Find first and last keys
    try:
        fullKeyList = sorted(mc.keyframe(selObj, q=1))
        firstLastKeys = fullKeyList[0], fullKeyList[-1]
        # Bake
        mc.bakeResults(bakeObj, time=firstLastKeys)
    except:
        pass


locTool()
