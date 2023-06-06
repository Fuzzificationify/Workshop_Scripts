import sys
from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtGui
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.cmds as mc
import pymel.core as pm
from Helper_Functions import ui_premades
from Helper_Functions import maya_helpers




def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    if sys.version_info.major >= 3:
        return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

    else:
        return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


class LocatorLister(QtWidgets.QDialog):
    def __init__(self, parent=maya_main_window()):
        super(LocatorLister, self).__init__(parent)
        self.setWindowTitle("Locator_Lister")
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
        self.make_labels()

    def create_layouts(self):
        base_layout = QtWidgets.QVBoxLayout()
        rows_dic = {}

        for label_list in self.loc_label_dic.values():
            rows_dic[label_list[0]] = QtWidgets.QHBoxLayout()

            for label in label_list:
                rows_dic[label_list[0]].addWidget(label)

        # # OK Cancel Buttons
        # button_layout = QtWidgets.QHBoxLayout()
        # button_layout.addStretch()
        # button_layout.addWidget(self.ok_btn)
        # button_layout.addWidget(self.cancel_btn)

        # Main Layout

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setSpacing(4)
        main_layout.setContentsMargins(6, 12, 6, 6)

        for row in rows_dic.values():
            base_layout.addLayout(row)

        main_layout.addLayout(base_layout)
        main_layout.addSpacing(9)

        # main_layout.addLayout(button_layout)
        main_layout.addSpacing(5)

    def create_connections(self):
        pass

    def make_labels(self):
        self.loc_label_dic = {}
        #self.master_label_dic = {}
        self.find_locators()
        #self.get_masters(self.my_loc_list)

        for loc in self.my_loc_list:
            # Make a 3 part list of the loc, the master, and the constrain check
            # Store list in a dictionary
            loc_label = QtWidgets.QLabel(str(loc))

            master = loc.master.get()
            master_label = QtWidgets.QLabel(str(master))

            constrain_check = self.loc_dic[loc]
            constrain_check_label = QtWidgets.QLabel(str(constrain_check))

            self.loc_label_dic[loc] = [loc_label, master_label, constrain_check_label]

    def get_masters(self, loc_list):
        self.master_list = [loc.master.get() for loc in loc_list]

    def find_locators(self):
        locs = pm.ls(type="locator")
        self.loc_dic = {}
        self.my_loc_list = []

        for loc in locs:
            xform_loc = loc.getParent()

            if xform_loc.hasAttr('master'):
                self.my_loc_list.append(xform_loc)
                self.get_object(xform_loc)
        print(self.loc_dic)

    def get_object(self, loc):
        self.loc_dic[loc] = False

        # Find connected constraint
        constraint = loc.listConnections(type="constraint")
        print(constraint)

        for con in constraint:
            connections = []
            transforms = con.listConnections(scn=1, type="transform", exactType=1, d=0)
            joints = con.listConnections(scn=1, type="joint", exactType=1, d=0)

            if transforms: connections.extend(transforms)
            if joints: connections.extend(joints)

            obj_from_master = loc.master.get()
            obj_from_connection = list(set(connections))

            if obj_from_master in obj_from_connection:
                self.loc_dic[loc] = True


if __name__ == "__main__":
    try:
        loc_lister.close()  # pylint: disable=E0601
        loc_lister.deleteLater()

    except:
        pass

    loc_lister = LocatorLister()
    loc_lister.show()
