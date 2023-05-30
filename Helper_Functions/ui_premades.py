# Premade Widget Combo's for common situations
from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtGui
from shiboken2 import wrapInstance

import ast

import maya.cmds as mc
from Helper_Functions import keyframe_helpers as kh

class MyDoubleSpinBox(QtWidgets.QDoubleSpinBox):
    def __init__(self, parent=None):
        super(MyDoubleSpinBox, self).__init__(parent)

        self.setRange(-1000, 999999)
        self.setDecimals(0)
        self.setSingleStep(1)
        self.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.setAlignment(QtCore.Qt.AlignCenter)

        # clear focus after pressing enter key
        self.editingFinished.connect(self.clearFocus)


class DoubleClickBtn(QtWidgets.QPushButton):
    rightClicked = QtCore.pyqtSignal()
    doubleClicked = QtCore.pyqtSignal()

    def __init__(self, parent = None):
        super(DoubleClickBtn, self).__init__(parent)
        self.is_pressed = False

    @QtCore.pyqtSlot()
    def mouseDoubleClickEvent(self, event):
        self.doubleClicked.emit()

    @QtCore.pyqtSlot()
    def mousePressEvent(self, event):
        super(DoubleClickBtn, self).mousePressEvent(event)
        if event.button() == QtCore.Qt.RightButton:
            self.rightClicked.emit()


class SimpleSourcer(QtWidgets.QWidget):
    def __init__(self, Dialogue):
        super(SimpleSourcer, self).__init__()

        self.result_layout = QtWidgets.QHBoxLayout()
        self.result_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.result_layout)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        self.sel_line_edit = QtWidgets.QLineEdit()
        self.sel_line_edit.setEnabled(False)
        self.store_sel_btn = DoubleClickBtn(self)
        self.store_sel_btn.setIcon(QtGui.QIcon(":selectByObject.png"))


    def create_layouts(self):
        self.result_layout.addWidget(self.sel_line_edit)
        self.result_layout.addWidget(self.store_sel_btn)


    def populate(self):
        self.selection = self.maya_get_selection()
        self.sel_line_edit.setText(str(self.selection))
        self.sel_line_edit.setStyleSheet("QLineEdit { color: white; background-color: Sienna }")

    def maya_get_selection(self):
        return mc.ls(sl=1)

    def maya_select(self):
        selection = ast.literal_eval( self.sel_line_edit.text() ) # Make sure it's type is a real list
        mc.select(selection)

    def create_connections(self):
        self.store_sel_btn.clicked.connect(self.populate)
        self.store_sel_btn.rightClicked.connect(self.maya_select)


class SourcingWidget(QtWidgets.QWidget):

    def __init__(self, Dialogue, TitleText="Title", RowText=""):
        super(SourcingWidget, self).__init__()
        self.dialogue = Dialogue
        self.TitleText = TitleText
        self.RowText = RowText

        self.result_layout = QtWidgets.QHBoxLayout()
        self.result_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.result_layout)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        self.qlist = QtWidgets.QListWidget()
        self.qlist.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.qlist.setMaximumSize(150, 57)

        self.add_btn = QtWidgets.QPushButton("")
        self.add_btn.setIcon(QtGui.QIcon(":addCreateGeneric.png"))
        self.add_btn.setFixedSize(27,23)

        self.remove_btn = DoubleClickBtn("")
        self.remove_btn.setIcon(QtGui.QIcon(":deleteClip.png"))
        self.remove_btn.setFixedSize(27,23)

    def create_layouts(self):
        self.source_sel_layout = QtWidgets.QHBoxLayout()
        self.source_sel_layout.setContentsMargins(0, 1, 1, 1)
        self.source_sel_layout.addWidget(self.qlist)
        self.source_sel_layout.addStretch()
        self.source_sel_layout.addWidget(self.add_btn)
        self.source_sel_layout.addStretch()
        self.source_sel_layout.addWidget(self.remove_btn)
        self.source_sel_layout.addStretch()

        self.result_layout.addLayout(self.source_sel_layout)

    def create_connections(self):
        self.qlist.itemSelectionChanged.connect(self.sel_from_qlist)
        self.add_btn.clicked.connect(self.add_target)
        self.remove_btn.clicked.connect(self.clear_target)

        self.remove_btn.clicked.connect(self.clear_target)
        self.remove_btn.doubleClicked.connect(self.clear_qlist_all)
        self.remove_btn.rightClicked.connect(self.clear_qlist_all)

    def sel_from_qlist(self):
        items = self.qlist.selectedItems()
        self.selection = [i.text() for i in items]
        # Select in Maya Object
        mc.select(self.selection)

    def clear_qlist_sel(self):
        self.qlist.clearSelection()

    def clear_qlist_all(self):
        self.qlist.clear()

    def get_all_items(self):
        self.item_strings = [str(self.qlist.item(i).text()) for i in range(self.qlist.count())]
        self.all_items = [self.qlist.item(i) for i in range(self.qlist.count())]



        return self.item_strings, self.all_items

    def add_target(self):
        self.get_all_items()
        targets = mc.ls(sl=1)

        # Add to QList if not already there
        for target in targets:
            if target in self.item_strings:
                pass
            else:
                self.qlist.addItem(str(target))

    def clear_target(self):
        targets =  self.qlist.selectedItems()
        for target in targets:
            self.qlist.takeItem(self.qlist.row(target))

            
class FrameRangeWidget(QtWidgets.QWidget):

    def __init__(self, Dialogue, TitleText="Frame Range"):
        super(FrameRangeWidget, self).__init__()
        self.dialogue = Dialogue
        self.TitleText = TitleText

        self.base_size = self.dialogue.size().height()

        self.result_layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.result_layout)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

        self.get_range()


    def create_widgets(self):
        self.start_dsb = MyDoubleSpinBox()
        self.end_dsb = MyDoubleSpinBox()

        self.range_spacer = QtWidgets.QLabel(" - ")

        # Get Range Button
        self.get_source_range_btn = QtWidgets.QPushButton("")
        self.get_source_range_btn.setIcon(QtGui.QIcon(":adjustTimeline.png"))

    def create_layouts(self):
        # Get range input layout
        get_range_layout = QtWidgets.QHBoxLayout()
        get_range_layout.addStretch()
        get_range_layout.addWidget(self.start_dsb)
        get_range_layout.addWidget(self.range_spacer)
        get_range_layout.addWidget(self.end_dsb)
        get_range_layout.addStretch()
        get_range_layout.addWidget(self.get_source_range_btn)
        get_range_layout.addStretch()

        form_layout = QtWidgets.QFormLayout()
        form_layout.setContentsMargins(0 ,0, 0, 0)
        form_layout.addRow("Frame Range:", get_range_layout)

        self.result_layout.addLayout(form_layout)
        self.result_layout.setContentsMargins(2, 0, 2, 8)

    def create_connections(self):
        self.get_source_range_btn.clicked.connect(self.get_range)

    def get_range(self):
        if kh.check_timeslider_sel():
            start_time, end_time = kh.get_timeslider_sel_range()
            # the red highlight in Maya looks like it's 1 less, so I'm making it what I think it should be
            end_time = end_time -1
        else:
            start_time, end_time = kh.get_scene_range()

        self.start_dsb.setValue(start_time)
        self.end_dsb.setValue(end_time)

        self.start_time = start_time
        self.end_time = end_time

