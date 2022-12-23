import pymel.core as pm
from Helper_Functions import ui_premades
reload(ui_premades)

# curv = pm.PyNode(pm.keyframe(q=1, n=1)[0])
# flex_key = pm.keyframe(q=1, selected=True, indexValue=1)[0]
# pre_flex_key = flex_key - 1
# key_list = pm.keyframe(q=1, selected=True, indexValue=1)
#
#
#
# flex_val = curv.getValue(flex_key)
# pre_flex_key_val = curv.getValue(pre_flex_key)
# first_mover_val = curv.getValue(key_list[0])
#
#
# ratio = (flex_val - pre_flex_key_val) / (first_mover_val - pre_flex_key_val)
# damping_factor = 0.5
#
# #######
#
# new_first_mover_val = curv.getValue(key_list[0])
#
# distance = new_first_mover_val - pre_flex_key_val
# desired_val = flex_val + distance * abs(ratio)
# new_flex_val = ((1 - damping_factor) * flex_val) + (damping_factor * desired_val)
#
# curv.setValue(flex_key, new_flex_val)


import sys

from PySide2 import QtCore
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui


def maya_main_window():
    """
    Return the Maya main window widget as a Python object
    """
    main_window_ptr = omui.MQtUtil.mainWindow()
    if sys.version_info.major >= 3:
        return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)
    else:
        return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)



class KeySourcer(ui_premades.SimpleSourcer):
    def __init__(self, parent=None):
        super(KeySourcer, self).__init__(parent)

    def maya_get_selection(self):

        self.curv = pm.PyNode(pm.keyframe(q=1, n=1)[0])
        self.key_indxs = pm.keyframe(q=1, selected=True, indexValue=1)
        print(self.curv, self.key_indxs)

        return self.key_indxs


class TestDialog(QtWidgets.QDialog):

    def __init__(self, parent=maya_main_window()):
        super(TestDialog, self).__init__(parent)

        self.setWindowTitle("Test Dialog")
        self.setMinimumWidth(200)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.curv = []
        self.damping_factor = 0.9

        self.create_widgets()
        self.create_layouts()
        self.create_connections()


    def create_widgets(self):
        self.flex_sourcer = KeySourcer("")
        self.mover_sourcer = KeySourcer("")

        self.set_ratio_btn = QtWidgets.QPushButton("Set")
        self.info_btn = QtWidgets.QPushButton("Info")

        self.slider = QtWidgets.QSlider()
        self.slider.setMinimum(-50)
        self.slider.setMaximum(50)
        self.slider.setValue(0)

        self.multi_spinb = QtWidgets.QDoubleSpinBox()
        self.multi_spinb.setValue(2)
        self.multi_spinb.setDecimals(2)

        self.ok_btn = QtWidgets.QPushButton("OK")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")


    def create_layouts(self):

        slide_layout = QtWidgets.QHBoxLayout()
        slide_layout.addWidget(self.slider)
        slide_layout.addSpacing(20)
        slide_layout.addWidget(self.multi_spinb)

        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow("Flexers:", self.flex_sourcer)
        form_layout.addRow("Movers:", self.mover_sourcer)
        form_layout.addRow("Set:", self.set_ratio_btn)
        form_layout.addRow("Info:", self.info_btn)

        form_layout.addRow("Slide:", slide_layout)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()

        button_layout.addWidget(self.ok_btn)
        button_layout.addWidget(self.cancel_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)

    def create_connections(self):
        self.set_ratio_btn.clicked.connect(self.get_ratio)
        self.info_btn.clicked.connect(self.print_info)
        self.slider.valueChanged.connect(self.slide_value)
        self.slider.valueChanged.connect(self.flex_it)
        self.ok_btn.clicked.connect(self.reset)
        self.ok_btn.clicked.connect(self.get_ratio)
        self.cancel_btn.clicked.connect(self.close)

    def get_info(self):
        self.post_keys_dic = {}
        self.key_ratio_dic = {}

        self.curv = self.flex_sourcer.curv
        self.flex_keys = self.flex_sourcer.key_indxs
        self.post_key = self.mover_sourcer.key_indxs[0]
        self.post_keys = self.mover_sourcer.key_indxs

        self.pre_val = self.curv.getValue(self.flex_keys[0] - 1)
        self.post_val = self.curv.getValue(self.post_key)

        self.pre_key_time = self.curv.getTime(self.flex_keys[0] - 1)

        for key in self.post_keys[1:]:
            val = self.curv.getValue(key)
            self.post_keys_dic[key] = val

        self.multi = self.multi_spinb.value()

    def reset(self):
        self.slider.blockSignals(True)
        self.slider.setValue(0)
        self.slider.blockSignals(False)

    def get_ratio(self):
        self.get_info()

        for key in self.flex_keys:
            key_val = self.curv.getValue(key)
            key_ratio = (key_val - self.pre_val) / (self.post_val - self.pre_val)

            self.key_ratio_dic[key] = (key_val, key_ratio)


    def slide_value(self):

        scaled_val = self.post_val + self.multi * self.slider.value()

        self.curv.setValue(self.post_key, scaled_val)
        print(self.post_keys_dic.items())
        for key, val in self.post_keys_dic.items():
            dif_val = scaled_val - self.post_val

            self.curv.setValue(key, val + dif_val)


    def set_ratio(self):
        self.get_info()
        self.ratio = (self.flex_val - self.pre_val) / (self.post_val - self.pre_val)


    def print_info(self):
        print('self.key_ratio_dic', self.key_ratio_dic)


    def flex_it(self):
        new_post_val = self.curv.getValue(self.post_key)
        distance = (new_post_val - self.pre_val)

        for key, val in self.key_ratio_dic.items():
            time_dif = self.curv.getTime(key) - self.pre_key_time
            old_val = self.curv.getValue(key)

            normalize_time_dif = 0.5 + (time_dif - 1) * 0.5 / (10 - 1)
            # result_val = dif_val * normalize_time_dif
            normalize_time_dif = max(normalize_time_dif, 0.5)
            normalize_time_dif = min(normalize_time_dif, 1)



            print('normalize_time_dif', normalize_time_dif)

            ratio = abs(val[1])
            new_val = self.damping_factor * (distance * ratio) + self.pre_val

            # wop = current_val * normalize_time_dif
            # result_val = new_val * normalize_time_dif

            result_val = (new_val - old_val) * normalize_time_dif

            print('new_val', new_val)
            print('old_val', old_val)
            print('result_val', result_val)

            self.curv.setValue(key, result_val)



    def get_key_values(self):
        self.curv = self.flex_sourcer.curv
        self.flex_key = self.flex_sourcer.key_indx
        self.post_key = self.mover_sourcer.key_indx

        flex_val = self.curv.getValue(self.flex_key)
        pre_val = self.curv.getValue(self.flex_key - 1)
        post_val = self.curv.getValue(self.post_key)


if __name__ == "__main__":

    try:
        test_dialog.close() # pylint: disable=E0601
        test_dialog.deleteLater()
    except:
        pass

    test_dialog = TestDialog()
    test_dialog.show()
