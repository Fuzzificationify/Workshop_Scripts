import sys

from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtGui
from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui
import maya.cmds as mc
import maya.mel as mel

from Helper_Functions import ui_premades
from Helper_Functions import maya_helpers

def maya_main_window():
    """
    Return the Maya main window widget as a Python object
    """
    main_window_ptr = omui.MQtUtil.mainWindow()
    if sys.version_info.major >= 3:
        return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)
    else:
        return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


class FancyCopyDialog(QtWidgets.QDialog):

    def __init__(self, parent=maya_main_window()):
        super(FancyCopyDialog, self).__init__(parent)

        self.setWindowTitle("FancyCopyDialog")
        self.setMinimumWidth(300)
        self.setMinimumHeight(90)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.setStyleSheet("QGroupBox { "
                               "font-weight: bold; "
                               "background-color: rgb(75, 75, 79);"
                               "border: 1px solid rgb(55, 55, 60);"
                               "border-radius: 4px;"
                               "margin-top: 6px;"
                                "padding: 10px 5px 0px 0px; "
                           "}"
                           "QGroupBox:title { "
                               "subcontrol-origin: margin; "
                                "left: 25px; "
                                "padding: 0px 5px 0px 5px; "
                           "}"
                            "QPushButton { "
                               "background-color: rgb(100, 103, 107); "
                                "padding: 7px; "
                           "}"
                            "QPushButton:hover { "
                                "background-color: rgb(130, 130, 145);"
                           "} "
                           "QPushButton:pressed { "
                                "background-color: rgb(50, 50, 50); "
                           "}");

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):

        # Instance Creation
        self.source_my_qlist = ui_premades.SourcingWidget(self)
        self.target_my_qlist = ui_premades.SourcingWidget(self)
        self.my_frame_range = ui_premades.FrameRangeWidget(self)

        self.include_nonKeyed_cb = QtWidgets.QCheckBox("Allow Non-keyed")
        self.include_nonKeyed_cb.setChecked(False)

        # Drop down channel box
        self.source_cbox = QtWidgets.QComboBox()
        self.source_cbox.setEnabled(False)
        self.all_channels_cb = QtWidgets.QCheckBox("All")
        self.all_channels_cb.setChecked(True)
        self.xform_only_cb = QtWidgets.QCheckBox("Xforms")
        self.xform_only_cb.setChecked(False)

        self.smart_select_btn = QtWidgets.QPushButton("")
        self.smart_select_btn.setIcon(QtGui.QIcon(":createSelectionSet.png"))
        self.smart_select_btn.setFixedSize(20,24)

        self.target_my_qlist.add_btn.setFixedSize(20, 24)
        self.target_my_qlist.remove_btn.setFixedSize(20, 24)

        self.target_cbox = QtWidgets.QComboBox()
        self.target_cbox.setEnabled(False)
        self.target_connect_cb = QtWidgets.QCheckBox("Connect")

        # Time and Value Offsets
        self.time_offset_le = QtWidgets.QLineEdit("0.0")
        self.time_offset_le.setMaximumWidth(40)
        self.value_offset_le = QtWidgets.QLineEdit("0.0")
        self.value_offset_le.setMaximumWidth(40)

        self.ok_btn = QtWidgets.QPushButton("OK")
        self.ok_btn.setMinimumWidth(90)
        self.cancel_btn = QtWidgets.QPushButton("Cancel")

    def create_layouts(self):

        self.frame_range_gbox_layout = QtWidgets.QVBoxLayout()
        self.frame_range_gbox_layout.setContentsMargins(4, 0, 2, 2)
        self.frame_range_gbox = QtWidgets.QGroupBox()
        self.frame_range_gbox.setContentsMargins(0, 0, 0, 0)

        self.frame_range_gbox.setLayout(self.frame_range_gbox_layout)
        self.frame_range_gbox_layout.addWidget(self.my_frame_range)

        source_cbox_layout = QtWidgets.QHBoxLayout()
        source_cbox_layout.addWidget(self.source_cbox)
        source_cbox_layout.addWidget(self.all_channels_cb)
        source_cbox_layout.addWidget(self.xform_only_cb)


        cb_hbox = QtWidgets.QHBoxLayout()
        cb_hbox.addSpacing(12)
        cb_hbox.addWidget(self.include_nonKeyed_cb)

        # Form layout (a layout composite)
        form_layout = QtWidgets.QFormLayout()
        form_layout.setSpacing(10)
        form_layout.addRow("Source Object:", self.source_my_qlist)
        form_layout.addRow("", cb_hbox)
        form_layout.addRow("Source Channel:", source_cbox_layout)

        # Source Groupboxing Form layout
        self.groupbox = QtWidgets.QGroupBox("Source for Copying")
        self.groupboxLayout = QtWidgets.QVBoxLayout()
        self.groupboxLayout.setContentsMargins(4, 6, 4, 6)
        self.groupbox.setLayout(self.groupboxLayout)

        self.groupboxLayout.addLayout(form_layout)

        # Target Channel ComboBox
        target_cbox_layout = QtWidgets.QHBoxLayout()
        target_cbox_layout.addWidget(self.target_cbox)
        target_cbox_layout.addWidget(self.target_connect_cb)

        # Time and Value Offsets
        self.time_val_form_layout = QtWidgets.QFormLayout()
        self.time_val_form_layout.addRow("Value Offset:", self.value_offset_le)

        self.time_val_form_layout2 = QtWidgets.QFormLayout()
        self.time_val_form_layout2.addRow("Time Offset:", self.time_offset_le)

        self.time_val_hbox = QtWidgets.QHBoxLayout()
        self.time_val_hbox.addSpacing(15)
        self.time_val_hbox.addLayout(self.time_val_form_layout)
        self.time_val_hbox.addLayout(self.time_val_form_layout2)
        self.time_val_hbox.addStretch()

        # Adding my extra 'Smart' Button to instance'd layout
        self.target_my_qlist.source_sel_layout.addWidget(self.smart_select_btn)
        self.target_my_qlist.source_sel_layout.setSpacing(1)

        target_form_layout = QtWidgets.QFormLayout()
        target_form_layout.setSpacing(12)
        target_form_layout.addRow("Target Objects:", self.target_my_qlist)
        target_form_layout.addRow("Target Channel:", target_cbox_layout)
        target_form_layout.addRow(self.time_val_hbox)


        # Target Groupboxing
        self.target_groupbox = QtWidgets.QGroupBox("Target for Pasting")
        self.target_groupboxLayout = QtWidgets.QVBoxLayout()
        self.target_groupbox.setLayout(self.target_groupboxLayout)

        self.target_groupboxLayout.setContentsMargins(4, 6, 4, 6)
        self.target_groupboxLayout.addLayout(target_form_layout)

        # OK Cancel Buttons
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.ok_btn)
        button_layout.addWidget(self.cancel_btn)

        # Main Layout
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setSpacing(4)
        main_layout.setContentsMargins(6, 12, 6, 6)

        main_layout.addWidget(self.groupbox)
        main_layout.addWidget(self.target_groupbox)
        # main_layout.addSpacing(5)
        main_layout.addWidget(self.frame_range_gbox)
        main_layout.addSpacing(9)
        main_layout.addLayout(button_layout)
        main_layout.addSpacing(5)

    def create_connections(self):

        self.all_channels_cb.clicked.connect(self.source_cbox_toggle)
        self.all_channels_cb.clicked.connect(self.transform_cbs_toggle)
        self.xform_only_cb.clicked.connect(self.source_cbox_toggle)
        self.xform_only_cb.clicked.connect(self.xform_cbs_toggle)
        self.source_my_qlist.add_btn.clicked.connect(lambda: self.get_sel(self.source_my_qlist))
        self.source_my_qlist.add_btn.clicked.connect(lambda: self.get_attrs_from_cbox(self.source_my_qlist))
        self.source_my_qlist.add_btn.clicked.connect(lambda: self.populate_source_cbox(self.source_my_qlist))

        self.target_my_qlist.add_btn.clicked.connect(lambda: self.get_sel(self.target_my_qlist))
        self.target_my_qlist.add_btn.clicked.connect(lambda: self.get_attrs_from_cbox(self.target_my_qlist))
        self.target_my_qlist.add_btn.clicked.connect(lambda: self.populate_target_cbox(self.target_my_qlist))

        self.smart_select_btn.clicked.connect(self.smart_target_fill)

        self.ok_btn.clicked.connect(self.copy_anim)
        self.cancel_btn.clicked.connect(lambda: self.close())

    def get_sel(self, qlist):
        # qlist_sel is the strings, qlist_items the item widg (needed for removing item)
        qlist.qlist_sel, qlist.qlist_items = qlist.get_all_items()

        if qlist == self.source_my_qlist:
            if self.include_nonKeyed_cb.isChecked() == False:

                # Remove items that have no keys
                for i, obj in enumerate(qlist.qlist_sel):
                    obj_keys = mc.keyframe(obj, q=1) or []
                    if obj_keys == []:
                        print("{0} has no keys, removing".format(obj))
                        qlist.qlist.takeItem(qlist.qlist.row(qlist.qlist_items[i]))


    def source_cbox_toggle(self):
        if self.all_channels_cb.isChecked() or self.xform_only_cb.isChecked():
            self.source_cbox.setEnabled(False)
            self.target_cbox.setEnabled(False)
        else:
            self.source_cbox.setEnabled(True)
            self.target_cbox.setEnabled(True)

    def xform_cbs_toggle(self):
        if self.xform_only_cb.isChecked():
            print('doop')
            self.all_channels_cb.setChecked(False)

    def transform_cbs_toggle(self):
        if self.all_channels_cb.isChecked():
            print('boom')
            self.xform_only_cb.setChecked(False)

    def get_source_and_target_channel(self):
        if self.all_channels_cb.isChecked():
            self.source_channel = []
            self.target_channel = []
        elif self.xform_only_cb.isChecked():
            self.source_channel = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz']
            self.target_channel = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz']
        else:
            self.source_channel = self.source_cbox.currentText()
            self.target_channel = self.target_cbox.currentText()

    def get_attrs_from_cbox(self, qlist):
        self.source_channels_list = mc.listAttr(qlist.qlist_sel, keyable=1)
        self.source_channels_list = sorted(list(set(self.source_channels_list)))

        # Seperate out common transforms so they're in a normal order
        translates = [chan for chan in self.source_channels_list if "translate" in chan]
        rotates = [chan for chan in self.source_channels_list if "rotate" in chan]
        scale = [chan for chan in self.source_channels_list if "scale" in chan]

        transform_chans = [chan for chans in [translates, rotates, scale] for chan in chans]
        qlist.transform_chans = transform_chans

        others = [chan for chan in self.source_channels_list if chan not in transform_chans]
        qlist.others = others


    def populate_source_cbox(self, qlist):
        self.source_cbox.clear()

        for item in qlist.transform_chans:
            self.source_cbox.addItem(item)
        for item in qlist.others:
            self.source_cbox.addItem(item)

    def populate_target_cbox(self, qlist):
        self.target_cbox.clear()

        for item in qlist.transform_chans:
            self.target_cbox.addItem(item)
        for item in qlist.others:
            self.target_cbox.addItem(item)

    def get_range(self):
        aTimeSlider = mel.eval('$tmpVar=$gPlayBackSlider')
        self.timeRange = mc.timeControl(aTimeSlider, q=True, rangeArray=True)

        if mc.timeControl(aTimeSlider, q=True, rangeVisible=True):
            self.start_range.setText(str(self.timeRange[0]))
            self.end_range.setText(str(self.timeRange[1]))

        else:
            self.get_scene_range()
            self.start_range.setText(str(self.minTime))
            self.end_range.setText(str(self.maxTime))

    def get_all_targets(self):
        self.targets_all = self.target_my_qlist.get_all_items()

    def get_time_value_offsets(self):
        self.time_offset = float(self.time_offset_le.text())
        self.value_offset = float(self.value_offset_le.text())

    def get_ui_input(self):

        self.get_sel(self.source_my_qlist)
        self.get_sel(self.target_my_qlist)

        self.get_source_and_target_channel()

        # Get Time Range
        self.my_frame_range.get_range()
        self.time_range = (self.my_frame_range.start_time, self.my_frame_range.end_time)


        self.get_time_value_offsets()
        self.include_nonKeyed = self.include_nonKeyed_cb.isChecked()
        self.connect_val = self.target_connect_cb.isChecked()

    def smart_target_fill(self):
        self.get_sel(self.source_my_qlist)
        self.get_sel(self.target_my_qlist)

        self.source_objs = self.source_my_qlist.qlist_sel
        self.target_objs = self.target_my_qlist.qlist_sel

        # Check for namespace, and then run namespace switcher
        if maya_helpers.namespace_check(self.source_objs[0]):
            self.all_targets = maya_helpers.switch_namespace_selection(self.source_objs, self.target_objs)

            if self.all_targets == False: # Namespaces were the same
                self.same_rig_smart_fill()

        # Try substring replace if no namespace
        else:
            self.same_rig_smart_fill()

        self.target_my_qlist.get_all_items()
        self.target_my_qlist.qlist.clear()

        for target in self.all_targets:
                self.target_my_qlist.qlist.addItem(target)


    def same_rig_smart_fill(self):
        closest_source_obj = maya_helpers.find_closest_match(self.source_objs, self.target_objs[0])
        first_hit, last_hit, plus_string, minus_string = maya_helpers.get_delta_substrings(closest_source_obj, self.target_objs[0])
        self.all_targets = maya_helpers.smart_switch(self.source_objs, first_hit, last_hit, plus_string, minus_string)
        print("self.all_targets?", self.all_targets)

    def paste_one_to_one(self):
        for source, target in zip(self.sources_list, self.targets_list):
            source_keys = mc.keyframe(source, q=1) or []
            if source_keys == [] and self.include_nonKeyed == False:
                print("Skipping")
                continue
            if source_keys == [] and self.include_nonKeyed == True:
                mc.setKeyframe(source, time=self.time_range[0])

            mc.copyKey(source, time=self.time_range, attribute=self.source_channel)
            mc.pasteKey(target, attribute=self.target_channel, option="replace",
                        connect=self.connect_val, timeOffset=self.time_offset,
                        valueOffset=self.value_offset)

    def paste_one_to_many(self, source):
        source_keys = mc.keyframe(source, q=1) or []

        if source_keys == [] and self.include_nonKeyed == True:
            mc.setKeyframe(source, time=self.time_range[0])

        mc.copyKey(source, time=self.time_range, attribute=self.source_channel)

        for target in self.targets_list:

            mc.pasteKey(target, attribute=self.target_channel, option="replace",
                        connect=self.connect_val, timeOffset=self.time_offset,
                        valueOffset=self.value_offset)


     def copy_anim(self):
        self.get_ui_input()

        self.sources_list = self.source_my_qlist.qlist_sel
        self.targets_list = self.target_my_qlist.qlist_sel

        if len(self.sources_list) == 1:
            self.paste_one_to_many(self.sources_list[0])

        else:
            self.paste_one_to_one()



if __name__ == "__main__":

    try:
        fancy_copy.close() # pylint: disable=E0601
        fancy_copy.deleteLater()
    except:
        pass

    fancy_copy = FancyCopyDialog()
    fancy_copy.show()
