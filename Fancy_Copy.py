import sys

from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtGui
from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui
import maya.cmds as mc
import maya.mel as mel


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

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):

        self.ok_btn = QtWidgets.QPushButton("OK")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")

        # self.cube_btn = QtWidgets.QPushButton("Cube")

        # Selection Line Edit
        self.sel_line_edit = QtWidgets.QLineEdit()
        self.sel_line_edit.setMaximumWidth(180)
        self.store_sel_btn = QtWidgets.QPushButton("")
        self.store_sel_btn.setIcon(QtGui.QIcon(":selectByObject.png"))

        # Drop down channel box
        self.source_cbox = QtWidgets.QComboBox()

        # Range line edits
        self.start_range = QtWidgets.QLineEdit("1000")
        self.start_range.setAlignment(QtCore.Qt.AlignCenter)
        self.start_range.setMaximumWidth(40)
        self.end_range = QtWidgets.QLineEdit("1050")
        self.end_range.setAlignment(QtCore.Qt.AlignCenter)
        self.end_range.setMaximumWidth(40)

        self.range_spacer = QtWidgets.QLabel(" - ")

        # Get Range Button
        self.get_source_range_btn = QtWidgets.QPushButton("")
        self.get_source_range_btn.setIcon(QtGui.QIcon(":adjustTimeline.png"))



        # Target List
        self.target_qlist = QtWidgets.QListWidget()
        self.target_qlist.setMaximumSize(100, 30)
        self.target_qlist.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.target_qlist.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        # self.target_qlist.addItem("YEP")

        self.add_target_btn = QtWidgets.QPushButton("")
        self.add_target_btn.setIcon(QtGui.QIcon(":addCreateGeneric.png"))
        self.add_target_btn.setFixedSize(27,23)

        self.remove_target_btn = QtWidgets.QPushButton("")
        self.remove_target_btn.setIcon(QtGui.QIcon(":deleteClip.png"))
        self.remove_target_btn.setFixedSize(27,23)

        self.target_cbox = QtWidgets.QComboBox()
        self.target_connect_cb = QtWidgets.QCheckBox("Connect")

        # Time and Value Offsets
        self.time_offset_le = QtWidgets.QLineEdit("0.0")
        self.time_offset_le.setMaximumWidth(40)
        self.value_offset_le = QtWidgets.QLineEdit("0.0")
        self.value_offset_le.setMaximumWidth(40)

    def create_layouts(self):

        # Selection Chain Layout
        sel_layout = QtWidgets.QHBoxLayout()
        sel_layout.addWidget(self.sel_line_edit)
        sel_layout.addWidget(self.store_sel_btn)

        # Source range input layout
        source_range_layout = QtWidgets.QHBoxLayout()
        source_range_layout.addWidget(self.start_range)
        source_range_layout.addWidget(self.range_spacer)
        source_range_layout.addWidget(self.end_range)
        source_range_layout.addStretch()
        source_range_layout.addWidget(self.get_source_range_btn)

        # Form layout (a layout composite)
        form_layout = QtWidgets.QFormLayout()
        # form_layout.addRow(self.cube_btn)
        form_layout.addRow("Source Object:", sel_layout)
        form_layout.setSpacing(12)
        form_layout.addRow("Source Channel:", self.source_cbox)
        form_layout.addRow("Frame Range:", source_range_layout)

        # Source Groupboxing Form layout
        self.groupbox = QtWidgets.QGroupBox("Source for Copying")
        self.groupboxLayout = QtWidgets.QVBoxLayout()
        self.groupbox.setLayout(self.groupboxLayout)

        self.groupboxLayout.addLayout(form_layout)

        # OK Cancel Buttons
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.ok_btn)
        button_layout.addWidget(self.cancel_btn)


        # Target Layout
        target_sel_layout = QtWidgets.QHBoxLayout()
        target_sel_layout.addWidget(self.target_qlist)
        target_sel_layout.addWidget(self.add_target_btn)
        target_sel_layout.addWidget(self.remove_target_btn)

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

        target_form_layout = QtWidgets.QFormLayout()
        target_form_layout.addRow("Target Objects:", target_sel_layout)
        target_form_layout.setSpacing(12)
        target_form_layout.addRow("Target Channel:", target_cbox_layout)
        target_form_layout.addRow(self.time_val_hbox)

        # Target Groupboxing
        self.target_groupbox = QtWidgets.QGroupBox("Target for Pasting")
        self.target_groupboxLayout = QtWidgets.QVBoxLayout()
        self.target_groupbox.setLayout(self.target_groupboxLayout)

        self.target_groupboxLayout.addLayout(target_form_layout)



        # Main Layout
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.groupbox)
        main_layout.addWidget(self.target_groupbox)
        # main_layout.addLayout(self.time_val_hbox)
        main_layout.insertSpacing(10, 20)
        main_layout.addLayout(button_layout)

    def create_connections(self):
        # self.cube_btn.clicked.connect(self.cube)

        self.store_sel_btn.clicked.connect(self.get_sel)
        self.store_sel_btn.clicked.connect(self.populate_source_cbox)

        self.get_source_range_btn.clicked.connect(self.get_range)

        self.add_target_btn.clicked.connect(self.add_target)
        self.add_target_btn.clicked.connect(self.populate_target_cbox)
        self.remove_target_btn.clicked.connect(self.clear_target)

        self.ok_btn.clicked.connect(self.copy_anim)

    def cube(self):
        mc.polyCube(n="My_Copy_Cube")


    def get_sel(self):
        self.selection = mc.ls(sl=1)[0]
        self.sel_line_edit.setText(str(self.selection))
        self.sel_line_edit.setStyleSheet("QLineEdit { background-color: Sienna }")

    def populate_source_cbox(self):
        self.source_channels_list = mc.listAttr(self.selection, keyable=1)

        # Put visibility channel at the back
        if self.source_channels_list[0] == 'visibility':
            self.source_channels_list += [self.source_channels_list.pop(0)]

        self.source_cbox.clear()

        for item in self.source_channels_list:
            self.source_cbox.addItem(item)

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

    def get_scene_range(self):
        self.minTime = mc.playbackOptions(q=1, minTime=1)
        self.maxTime = mc.playbackOptions(q=1, maxTime=1)

        self.range_minTime = mc.playbackOptions(q=1, animationStartTime=1)
        self.range_maxTime = mc.playbackOptions(q=1, animationEndTime=1)


    def add_target(self):
        self.get_all_targets()

        targets = mc.ls(sl=1)
        # Add to QList if not already there
        for target in targets:
            if target in self.targets_all:
                pass
            else:
                self.target_qlist.addItem(str(target))
        self.target_qlist.setFixedSize(100, self.target_qlist.sizeHintForRow(0) * self.target_qlist.count() + 2 * self.target_qlist.frameWidth())


    def clear_target(self):
        targets =  self.target_qlist.selectedItems()
        for target in targets:
            self.target_qlist.takeItem(self.target_qlist.row(target))

        if self.target_qlist.count() == 0:
            self.target_cbox.clear()


    def populate_target_cbox(self):
        self.target_channels_list = []

        self.get_all_targets()

        for item in self.targets_all:
            channels = mc.listAttr(item, keyable=1)
            self.target_channels_list.append(channels)

        # Flatten List, remove duplicate channels
        self.target_channels_list = [val for sublist in self.target_channels_list for val in sublist]
        self.target_channels_list = list(dict.fromkeys(self.target_channels_list))

        # Put visibility channel at the back
        print(self.target_channels_list)
        if self.target_channels_list[0] == 'visibility':
            self.target_channels_list += [self.target_channels_list.pop(0)]

        self.target_cbox.clear()

        for item in self.target_channels_list:
            self.target_cbox.addItem(item)

    def get_all_targets(self):
        self.targets_all = [str(self.target_qlist.item(i).text()) for i in range(self.target_qlist.count())]

    def copy_anim(self):
        self.connect_val = self.target_connect_cb.isChecked()
        self.source_channel = self.source_cbox.currentText()
        self.target_channel = self.target_cbox.currentText()

        # Get Time Range
        start = int(float(self.start_range.text()))
        end = int(float(self.end_range.text()))
        time_range = (start, end)

        # Copy Keys
        mc.copyKey(self.selection, time=time_range, attribute=self.source_channel)

        # Get Offsets
        self.get_time_value_offsets()

        # Paste Keys
        for target in self.targets_all:
            mc.pasteKey(target, attribute=self.target_channel, option="replace",
                        connect=self.connect_val, timeOffset=self.time_offset, valueOffset=self.value_offset)

    def get_time_value_offsets(self):
        self.time_offset = float(self.time_offset_le.text())
        self.value_offset = float(self.value_offset_le.text())


if __name__ == "__main__":

    try:
        fancy_copy.close() # pylint: disable=E0601
        fancy_copy.deleteLater()
    except:
        pass

    fancy_copy = FancyCopyDialog()
    fancy_copy.show()

