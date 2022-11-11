import sys

from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtGui
from shiboken2 import wrapInstance

import maya.cmds as mc
import maya.mel as mel
import maya.OpenMayaUI as omui
from maya.api import OpenMaya as om

def maya_main_window():
    """
    Return the Maya main window widget as a Python self.object
    """
    main_window_ptr = omui.MQtUtil.mainWindow()
    if sys.version_info.major >= 3:
        return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)
    else:
        return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

class NurbsPathDialog(QtWidgets.QDialog):

    def __init__(self, parent=maya_main_window()):
        super(NurbsPathDialog, self).__init__(parent)

        self.setWindowTitle("Nurbs Path")
        self.setMaximumWidth(200)
        self.setMaximumHeight(90)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()


    def create_widgets(self):

        self.make_nurbs_btn = QtWidgets.QPushButton("Make Nurbs Curve")
        self.update_anim_btn = QtWidgets.QPushButton("Update Anim")
        self.smooth_nurbs_btn = QtWidgets.QPushButton("Smooth")

        #Dial
        self.smooth_dial = QtWidgets.QDial()
        self.smooth_dial.setNotchesVisible(True)
        self.smooth_dial.setRange(01, 9)
        self.smooth_dial.setValue(2)
        self.smooth_dial.setFocusPolicy(QtCore.Qt.NoFocus)
        self.dial_label = QtWidgets.QLabel("Smooth Value = 2")


    def create_layouts(self):

        dial_layout = QtWidgets.QHBoxLayout()
        dial_layout.addWidget(self.smooth_nurbs_btn)
        dial_layout.addWidget(self.smooth_dial)
        dial_layout.addWidget(self.dial_label)
        dial_layout.setSpacing(11)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.make_nurbs_btn)
        main_layout.addLayout(dial_layout)
        main_layout.addWidget(self.update_anim_btn)

    def create_connections(self):
        self.make_nurbs_btn.clicked.connect(self.make_nurbs)
        self.update_anim_btn.clicked.connect(self.update_anim)
        self.smooth_nurbs_btn.clicked.connect(self.smooth_nurbs_A)

        self.smooth_dial.valueChanged.connect(lambda: self.dial_label.setText("Smooth Value = " + str(self.smooth_dial.value())))


    def make_nurbs(self):
        positions = []
        self.obj = mc.ls(sl=1)[0]

        self.minTime = mc.playbackOptions(q=1, minTime=1)
        self.maxTime = mc.playbackOptions(q=1, maxTime=1)

        for frame in range(int(self.minTime), int(self.maxTime)):
            # Get worldspace using end of .worldMatrix (last 4 values)
            valueList = mc.getAttr((self.obj+'.worldMatrix'),time=(frame))

            x = valueList[-4]
            y = valueList[-3]
            z = valueList[-2]
            trans = [x, y, z]

            positions.append(trans)

        # Make Curve
        name_no_namespace = self.obj.rpartition(":")[2]
        curv_name = name_no_namespace + "_curv"

        self.curv = mc.curve(name=curv_name, p=positions)

        #Rename shape
        shape = mc.listRelatives(self.curv, shapes=1)[0]
        mc.rename(shape, "{0}Shape".format(curv_name))


    def update_anim(self):
        new_positions = []

        #get CV count
        CV_count = mc.getAttr(self.curv + '.cp', s=1)

        for cv in range(CV_count):
            cv_pos = mc.pointPosition('{0}.cv[{1}]'.format(self.curv, cv))

            # Confusing Matrix maths o.o
            target_iv = mc.getAttr(self.obj + ".worldInverseMatrix")
            target_local = mc.getAttr(self.obj + ".matrix")

            source_mat = om.MPoint(cv_pos)
            tar_iv_mat = om.MMatrix(target_iv)
            tar_loc_mat = om.MMatrix(target_local)

            full_tar_mat = tar_iv_mat * tar_loc_mat
            cv_pos_true = source_mat * full_tar_mat

            #cv_pos = mc.pointPosition('{0}.cv[{1}]'.format(self.curv, cv))
            new_positions.append(cv_pos_true)

        for pos in range(CV_count):
            time = pos + self.minTime
            mc.setKeyframe(self.obj, at='translateX', value = new_positions[pos][0], time = time)
            mc.setKeyframe(self.obj, at='translateY', value = new_positions[pos][1], time = time)
            mc.setKeyframe(self.obj, at='translateZ', value = new_positions[pos][2], time = time)


    def smooth_nurbs_A(self):
        self.smooth_val = self.smooth_dial.value()
        mel.eval("modifySelectedCurves smooth {0} 0;".format(self.smooth_val))

    def smooth_nurbs_B(self):
        cvs = mc.ls(sl=1)[0]
        curve = cvs.split('.')[0]

        mc.smoothCurve(cvs, s=3, rpo=1)

        mc.select(curve)
        mc.selectMode(component=1)
        mc.select(cvs)


if __name__ == "__main__":

    try:
        nurbs_path.close() # pylint: disable=E0601
        nurbs_path.deleteLater()
    except:
        pass

    nurbs_path = NurbsPathDialog()
    nurbs_path.show()
