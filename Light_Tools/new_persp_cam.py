import maya.cmds as cmds

# To Do: Copy Camera attributes (?) (So long as it doesn't copy the error too)

def fixThePerspCamera():
    perCam = 'persp'
    n_clip, f_clip = get_cam_attrs(perCam)

    mc.camera(perCam, e=True, sc=False)
    mc.delete(perCam)

    newCam = mc.camera()
    mc.rename(newCam[0], 'persp')
    mc.camera('persp', e=True, sc=True)
    mc.setAttr('persp.nearClipPlane', n_clip)
    mc.setAttr('persp.farClipPlane', f_clip)

    mc.lookThru('persp')
    mc.hide('persp')


def get_cam_attrs(cam):
    near_clip_plane = ".nearClipPlane"
    far_clip_plane = ".farClipPlane"

    n_clip_plane_val = mc.getAttr(cam + near_clip_plane)
    f_clip_plane_val = mc.getAttr(cam + far_clip_plane)

    return n_clip_plane_val, f_clip_plane_val


fixThePerspCamera()
