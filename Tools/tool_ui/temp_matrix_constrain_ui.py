"""
To Do / Bugs:
- Ignore locked channels when constraining
- Stop reset of Time Range after running
- Stop Unkeys all extra attributes
"""


import sys

from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtGui
from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui
import maya.cmds as mc
import maya.mel as mel

from Helper_Functions import ui_premades
from Helper_Functions import keyframe_helpers as kh
from My_Tools import temp_matrix_constrain


def maya_main_window():
    """
    Return the Maya main window widget as a Python object
    """
    main_window_ptr = omui.MQtUtil.mainWindow()
    if sys.version_info.major >= 3:
        return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)
    else:
        return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

class UndoContext(object):
    def __enter__(self):
        cmds.undoInfo(openChunk=True)
    def __exit__(self, *exc_info):
        cmds.undoInfo(closeChunk=True)

class SourcingWidget(QtWidgets.QWidget):

    def __init__(self, Dialogue, TitleText="Title", RowText=""):
        super(SourcingWidget, self).__init__()
        self.dialogue = Dialogue
        self.TitleText = TitleText
        self.RowText = RowText

        self.hasRun_marker = 0

        self.previous_qlist_size = 0
        self.base_size = self.dialogue.size().height()

        self.result_layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.result_layout)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()


    def create_widgets(self):
        self.qlist = QtWidgets.QListWidget()
        self.qlist.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.qlist.setMaximumSize(150, 30)
        self.qlist.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.qlist.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.add_btn = QtWidgets.QPushButton("")
        self.add_btn.setIcon(QtGui.QIcon(":addCreateGeneric.png"))
        self.add_btn.setFixedSize(27,23)

        self.remove_btn = QtWidgets.QPushButton("")
        self.remove_btn.setIcon(QtGui.QIcon(":deleteClip.png"))
        self.remove_btn.setFixedSize(27,23)

    def create_layouts(self):
        source_sel_layout = QtWidgets.QHBoxLayout()
        source_sel_layout.addWidget(self.qlist)
        source_sel_layout.addStretch()
        source_sel_layout.addWidget(self.add_btn)
        source_sel_layout.addWidget(self.remove_btn)
        source_sel_layout.addStretch()

        sourcing_form_layout = QtWidgets.QFormLayout()
        sourcing_form_layout.addRow(self.RowText, source_sel_layout)
        sourcing_form_layout.setSpacing(12)

        # Sourcing Groupboxing
        self.sourcing_groupbox = QtWidgets.QGroupBox(self.TitleText)
        self.sourcing_groupboxLayout = QtWidgets.QVBoxLayout()
        self.sourcing_groupbox.setLayout(self.sourcing_groupboxLayout)
        self.sourcing_groupboxLayout.addLayout(sourcing_form_layout)

        self.sourcing_groupbox.setContentsMargins(0,14,0,0)

        self.sourcing_groupbox.setStyleSheet("QGroupBox { background-color: \
                                            rgb(60, 60, 75); border: 11px solid rgb(50, 50, 55); }")

        self.result_layout.addWidget(self.sourcing_groupbox)

        self.result_layout.setContentsMargins(0,0,0,0)

    def create_connections(self):
        self.qlist.itemSelectionChanged.connect(self.sel_from_qlist)
        self.add_btn.clicked.connect(self.add_target)
        self.remove_btn.clicked.connect(self.clear_target)

    def add_num_prefix(self):
        for i in range(self.qlist.count()):
            text = self.qlist.item(i).text()
            body = text.split('. ')[-1]
            prefix = str(i) + '. '
            self.qlist.item(i).setText(prefix + body)

    def sel_from_qlist(self):
        items = self.qlist.selectedItems()
        self.selection = [i.text() for i in items]

        mc.select(self.selection)

    def clear_qlist_sel(self):
        self.qlist.clearSelection()

    def get_all_items(self):
        self.all_items = [str(self.qlist.item(i).text()) for i in range(self.qlist.count())]
        return self.all_items

    def add_target(self):

        if self.hasRun_marker == 0:
            self.base_size = self.dialogue.size().height()
        self.get_all_items()

        targets = mc.ls(sl=1)
        # Add to QList if not already there
        for target in targets:
            if target in self.all_items:
                pass
            else:
                self.qlist.addItem(str(target))


        qlist_size = self.qlist.sizeHintForRow(0) * self.qlist.count() + 2 * self.qlist.frameWidth()
        self.qlist.setFixedSize(180, qlist_size)
        self.dialogue.setFixedHeight(self.base_size + qlist_size)

        self.hasRun_marker = 1

    def clear_target(self):

        targets =  self.qlist.selectedItems()
        for target in targets:
            self.qlist.takeItem(self.qlist.row(target))

        qlist_size = self.qlist.sizeHintForRow(0) * self.qlist.count() + 2 * self.qlist.frameWidth()
        self.qlist.setFixedSize(180, qlist_size)

        self.dialogue.setFixedHeight(self.base_size + qlist_size)

class MatrixUI(QtWidgets.QDialog):

    def __init__(self, parent=maya_main_window()):
        super(MatrixUI, self).__init__(parent)

        self.setWindowTitle("MatrixUI")
        self.setMinimumWidth(300)
        self.setMinimumHeight(90)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.setStyleSheet( "QDialog { background-color: rgb(60, 60, 60); }"
                            "QPushButton { background-color: rgb(62, 71, 75); "
                            "border: 2px solid rgb(115, 115, 115); "
                            "padding: 6px; }"
                            
                            "QPushButton:hover { background-color: rgb(70, 95, 120); }"

                            "QGroupBox { background-color: \
                            rgb(60, 60, 75); border: 7px solid rgb(50, 50, 55); }"
                            )



        self.protectorKeys = 1
        self.constraints = []

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

        self.get_range_scene()


    def create_widgets(self):

        self.controlers_widg = ui_premades.SourcingWidget(self, TitleText="Get Controls", RowText="")
        self.locators_widg = ui_premades.SourcingWidget(self, TitleText="Get Locators", RowText="")
        # self.locators_widg = SourcingWidget(self, TitleText="Get Locators", RowText="")

        self.to_loc_btn = QtWidgets.QPushButton("To Locators")
        self.switch_btn = QtWidgets.QPushButton("Switch Back")
        self.del_constraints_btn = QtWidgets.QPushButton("Del Constraints")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")

        # Range line edits
        self.start_range_spin = ui_premades.MyDoubleSpinBox()
        self.end_range_spin = ui_premades.MyDoubleSpinBox()

        self.range_spacer = QtWidgets.QLabel(" - ")

        # Get Range Button
        self.get_source_range_btn = QtWidgets.QPushButton("")
        self.get_source_range_btn.setIcon(QtGui.QIcon(":adjustTimeline.png"))

        self.current_key_cb = QtWidgets.QCheckBox()

        # Check Box
        self.keys_cb = QtWidgets.QCheckBox("Only Keys")
        self.keys_cb.setChecked(1)


    def create_layouts(self):

        # Get range input layout
        get_range_layout = QtWidgets.QHBoxLayout()
        get_range_layout.addWidget(self.start_range_spin)
        get_range_layout.addWidget(self.range_spacer)
        get_range_layout.addWidget(self.end_range_spin)
        get_range_layout.addStretch()
        get_range_layout.addWidget(self.get_source_range_btn)

        # Form layout (a layout composite)
        form_layout = QtWidgets.QFormLayout()
        form_layout.setSpacing(12)
        form_layout.addRow("Frame Range:", get_range_layout)
        form_layout.addRow("Current Frame:", self.current_key_cb)

        # Get Range Groupboxing Form layout
        self.get_range_groupbox = QtWidgets.QGroupBox("Time Range")
        self.groupboxLayout = QtWidgets.QVBoxLayout()
        self.get_range_groupbox.setLayout(self.groupboxLayout)
        self.get_range_groupbox.setStyleSheet("QGroupBox { background-color: \
            rgb(60, 60, 75); border: 6px solid rgb(50, 50, 55); }")
        self.groupboxLayout.addLayout(form_layout)

        # Check box
        options_layout = QtWidgets.QHBoxLayout()
        options_layout.addStretch()
        options_layout.addWidget(self.del_constraints_btn)

        options_layout.addWidget(self.keys_cb)

        # Generate QLists in Groupboxes
        # self.controlers_widg = SourcingWidget(self, TitleText="Get Controls", RowText="")

        controller_layout = QtWidgets.QHBoxLayout()
        controller_layout.addWidget(self.controlers_widg)

        # Source Groupboxing Form layout
        self.ctrls_groupbox = QtWidgets.QGroupBox("Get Controls")
        self.ctrls_groupboxLayout = QtWidgets.QVBoxLayout()
        self.ctrls_groupboxLayout.setContentsMargins(15, 12, 4, 6)
        self.ctrls_groupbox.setLayout(self.ctrls_groupboxLayout)

        self.ctrls_groupboxLayout.addLayout(controller_layout)

        locator_layout = QtWidgets.QHBoxLayout()
        locator_layout.addWidget(self.locators_widg)

        # Source Groupboxing Form layout
        self.loc_groupbox = QtWidgets.QGroupBox("Get Locators")
        self.loc_groupboxLayout = QtWidgets.QVBoxLayout()
        self.loc_groupboxLayout.setContentsMargins(15, 12, 4, 6)
        self.loc_groupbox.setLayout(self.loc_groupboxLayout)

        self.loc_groupboxLayout.addLayout(locator_layout)


        # OK Cancel Buttons
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.to_loc_btn, 5)
        button_layout.addWidget(self.switch_btn, 5)
        button_layout.addStretch()
        button_layout.addWidget(self.cancel_btn)

        # Main Layout
        self.main_layout = QtWidgets.QVBoxLayout(self)

        self.main_layout.addWidget(self.ctrls_groupbox)
        self.main_layout.addWidget(self.loc_groupbox)
        self.main_layout.addWidget(self.get_range_groupbox)
        self.main_layout.addLayout(options_layout)
        self.main_layout.insertSpacing(10, 20)
        self.main_layout.addLayout(button_layout)


    def create_connections(self):

        self.get_source_range_btn.clicked.connect(self.get_range_scene)
        self.current_key_cb.clicked.connect(self.grey_out)

        self.to_loc_btn.clicked.connect(self.run)
        self.switch_btn.clicked.connect(self.switch_back)
        self.del_constraints_btn.clicked.connect(self.delete_constraints)

        self.cancel_btn.clicked.connect(lambda:self.close())

    def get_range_scene(self):
        if kh.check_timeslider_sel():
            start_time, end_time = kh.get_timeslider_sel_range()
            # the red highlight in Maya looks like it's 1 less, so I'm making it what I think it should be
            end_time = end_time -1
        else:
            start_time, end_time = kh.get_scene_range()

        self.start_range_spin.setValue(start_time)
        self.end_range_spin.setValue(end_time)

    def get_range_ui(self):

        self.start_time = self.start_range_spin.value()
        self.end_time = self.end_range_spin.value()

        self.current_key_checks()

    def current_key_checks(self):
        if self.current_key_cb.isChecked():
            self.start_time = temp_matrix_constrain.get_current_frame()
            self.end_time = self.start_time
            self.onlyKeys = 0
            self.protectorKeys = 0


    def grey_out(self):
        if self.current_key_cb.isChecked():
            self.start_range_spin.setEnabled(False)
            self.end_range_spin.setEnabled(False)
            self.start_range_spin.setStyleSheet("QLineEdit { background-color: gray }")
            self.end_range_spin.setStyleSheet("QLineEdit { background-color: gray }")
        else:
            self.start_range_spin.setEnabled(True)
            self.end_range_spin.setEnabled(True)
            self.start_range_spin.setStyleSheet("")
            self.end_range_spin.setStyleSheet("")

    def get_input(self):
        self.get_range_ui()
        if not self.current_key_cb.isChecked():
            self.onlyKeys = self.keys_cb.isChecked()

        self.controls = self.controlers_widg.get_all_items()[0] #[0] to get just the text values
        self.locators = self.locators_widg.get_all_items()[0]


   
    def run(self):
        self.get_input()
        with UndoContext():
            self.constraints = temp_matrix_constrain.main(self.controls, self.locators, self.start_time, self.end_time, self.onlyKeys)[2]

    def switch_back(self):
        self.get_input()
        with UndoContext():
            temp_matrix_constrain.bake_back(self.controls, self.locators, self.start_time, self.end_time, self.onlyKeys, self.protectorKeys)

    def delete_constraints(self):
        if self.constraints:
            temp_matrix_constrain.delete_constraints(self.constraints)

if __name__ == "__main__":

    try:
        temp_matrix.close() # pylint: disable=E0601
        temp_matrix.deleteLater()
    except:
        pass

    temp_matrix = MatrixUI()
    temp_matrix.show()
