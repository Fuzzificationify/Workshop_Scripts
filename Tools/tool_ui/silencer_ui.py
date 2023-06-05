import sys

from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

import maya.cmds as mc
import maya.OpenMayaUI as omui

from Helper_Functions import ui_premades
from Helper_Functions import keyframe_helpers as kh
from My_Tools import silencer


def maya_main_window():
    """
    Return the Maya main window widget as a Python object
    """
    main_window_ptr = omui.MQtUtil.mainWindow()
    if sys.version_info.major >= 3:
        return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)
    else:
        return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


class StyledItemDelegate(QtWidgets.QStyledItemDelegate):
    def sizeHint(self, option, index):
        s = super(StyledItemDelegate, self).sizeHint(option, index)
        if index.parent().isValid():
            s.setHeight(15)
        else:
            s.setHeight(30)

        if index.data() == None:
            s.setHeight(10)
        return s


class MyWidget(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(MyWidget, self).__init__(*args, **kwargs)
        self.setFixedWidth(50)
        self.layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(20,0,0,0)


        self.btn1 = ui_premades.DoubleClickBtn("")

        self.layout.addWidget(self.btn1)
        self.layout.addStretch()

# class MyProxyStyle(QProxyStyle):
#     pass
#     def pixelMetric(self, QStyle_PixelMetric, option=None, widget=None):
#
#         if QStyle_PixelMetric == QStyle.PM_SmallIconSize:
#             return 40
#         else:
#             return QProxyStyle.pixelMetric(self, QStyle_PixelMetric, option, widget)



# class CustomStyle(QtGui.QStyle):
#     def __init__(self, color, parent=None):
#         super(CustomStyle, self).__init__(parent)
#         self.color = color
#
#     def drawPrimitive(self, element, option, painter, widget=None):
#         if element == QtGui.QStyle.PE_IndicatorBranch:
#
#             painter.setBrush(self.color)
#
#             super().drawPrimitive(element, option, painter, widget)

class Silencer(QtWidgets.QDialog):
    WINDOW_TITLE = "Shhhhhhhhhh"

    def __init__(self, parent=maya_main_window()):
        super(Silencer, self).__init__(parent)

        self.setWindowTitle(self.WINDOW_TITLE)
        if mc.about(ntOS=True):
            self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        elif mc.about(macOS=True):
            self.setWindowFlags(QtCore.Qt.Tool)

        self.setMinimumWidth(350)
        self.setMinimumWidth(350)

        self.btn_dic = {}
        self.flag = 0
        self.brush = QtGui.QBrush(QtGui.QColor(160, 60, 85))

        # Icons
        self.transform_icon = QtGui.QIcon(":polyCleanup.png")
        self.translate_icon = QtGui.QIcon(":move_M.png")
        self.rotate_icon = QtGui.QIcon(":rotate_M.png")
        self.other_icon = QtGui.QIcon(":pickOtherComp")

        self.create_widgets()
        self.create_layout()
        self.create_connections()

        self.refresh_tree_widget()

    def create_widgets(self):
        self.tree_widget = QtWidgets.QTreeWidget()

        self.tree_widget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.tree_widget.setContentsMargins(5, 5, 500, 5)
        self.tree_widget.setAlternatingRowColors(True)
        self.tree_widget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tree_widget.setMaximumWidth(350)

        self.tree_widget.header().setResizeMode(QtWidgets.QHeaderView.Fixed)

        header = QtWidgets.QTreeWidgetItem(["Transform Select:", "Objects:", "Mute:"])
        self.tree_widget.setHeaderItem(header)
        self.tree_widget.header().setStretchLastSection(True)

        self.tree_widget.setColumnWidth(1, 130)
        self.tree_widget.setColumnWidth(0, 130)
        self.tree_widget.setColumnWidth(2, 50)
        self.tree_widget.setFocusPolicy(QtCore.Qt.NoFocus)

        delegate = StyledItemDelegate(self.tree_widget)
        self.tree_widget.setItemDelegate(delegate)

        self.tree_widget.setColumnCount(3)
        self.tree_widget.header().swapSections(1, 0)

        self.mute_all_btn = QtWidgets.QPushButton("Mute All")
        self.unmute_all_btn = QtWidgets.QPushButton("Unmute All")

        self.refresh_btn = QtWidgets.QPushButton("Refresh")


        self.setStyleSheet("""
             QTreeView QHeaderView:section {
                background-color: rgb(64,64,84);
                color: rgb(193,193,193);
            }

            QTreeView::branch::closed::has-children {
                image: url(":teRightArrow.png");
            }

            QTreeView::branch::open::has-children {
                image: url(":teDownArrow.png");
            }
            
            QPushButton { 
                background-color: rgb(70, 90, 107); 
                padding: 7px; 
                           }
        """)


    def create_layout(self):
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.mute_all_btn)
        button_layout.addWidget(self.unmute_all_btn)
        button_layout.addSpacing(20)
        button_layout.addWidget(self.refresh_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(2, 2, 2, 2)
        main_layout.setSpacing(2)
        main_layout.addWidget(self.tree_widget)
        main_layout.addLayout(button_layout)

    def create_connections(self):
        self.refresh_btn.clicked.connect(self.refresh_tree_widget)
        self.mute_all_btn.clicked.connect(self.mute_all)
        self.unmute_all_btn.clicked.connect(self.unmute_all)

        self.tree_widget.itemSelectionChanged.connect(self.select_object)
        
    def dynamic_connections(self):
        helper = lambda i: (lambda: self.mute_btn_press(i))
        for btn in self.btn_dic.values():
            btn.btn1.clicked.connect(helper(btn))


    def row_highlight(self, item, row, btn):
        if btn.btn1.is_pressed == 1:
            if self.tree_widget.indexOfTopLevelItem(item) == row:
                item.setData(0, QtCore.Qt.BackgroundRole, None)
                item.setData(1, QtCore.Qt.BackgroundRole, None)
                item.setData(2, QtCore.Qt.BackgroundRole, None)

                btn.btn1.setIcon(QtGui.QIcon(":teMuteSoloOn.png"))

                btn.btn1.is_pressed = 0

        elif self.tree_widget.indexOfTopLevelItem(item) == row:
            item.setBackground(0, self.brush)
            item.setBackground(1, self.brush)
            item.setBackground(2, self.brush)

            btn.btn1.setIcon(QtGui.QIcon(":muted.png"))

            btn.btn1.is_pressed = 1


    def refresh_tree_widget(self):
        self.tree_widget.clear()
        self.btn_dic = {}

        pre_muted = silencer.get_scene_muted_objs()

        selected_objects = silencer.get_selected_objects()
        all_objects = list( set(pre_muted + selected_objects) )

        # Dummy row for top margin
        dummy_row = QtWidgets.QTreeWidgetItem()
        dummy_row.setDisabled(1)
        self.tree_widget.addTopLevelItem(dummy_row)

        for obj in all_objects:
            self.btn_dic["{}".format(obj)] = MyWidget()
            self.btn_dic["{}".format(obj)].btn1.setFixedSize(30, 25)
            self.btn_dic["{}".format(obj)].btn1.setIcon(QtGui.QIcon(":teMuteSoloOn.png"))
            item = self.create_item(obj, self.btn_dic["{}".format(obj)])

        self.click_btn_if_muted()
        self.dynamic_connections()

    def create_item(self, obj, btn):
        top_level_items = QtWidgets.QTreeWidgetItem(["All Transforms", obj, ""])
        top_level_items.setIcon(1, self.transform_icon)
        top_level_items.setFlags(top_level_items.flags() | QtCore.Qt.ItemIsTristate | QtCore.Qt.ItemIsUserCheckable)
        top_level_items.setCheckState(1, QtCore.Qt.Checked)

        self.tree_widget.addTopLevelItem(top_level_items)
        self.tree_widget.setItemWidget(top_level_items, 2, btn)

        self.create_children(top_level_items)
        #
        return top_level_items

    def create_children(self, parent):
        self.translate_chans, \
        self.rotate_chans, \
        self.other_chans = silencer.get_attrs_from_cbox(parent.text(1))

        translate = self.create_checkable_items(parent, name="Translate")
        translate.setIcon(0, self.translate_icon)
        translate.setForeground(0, QtGui.QBrush(QtGui.QColor(240, 195, 45)))

        rotate = self.create_checkable_items(parent, name="Rotate")
        rotate.setIcon(0, self.rotate_icon)
        rotate.setForeground(0, QtGui.QBrush(QtGui.QColor(120, 150, 210)))

        other = self.create_checkable_items(parent, name="Other")
        other.setIcon(0, self.other_icon)
        other.setForeground(0, QtGui.QBrush(QtGui.QColor(90, 240, 160)))

        channel_children = []

        for chan in self.translate_chans:
            item = self.create_checkable_items(translate, chan)
            channel_children.append(item)
        for chan in self.rotate_chans:
            item = self.create_checkable_items(rotate, chan)
            channel_children.append(item)
        for chan in self.other_chans:
            item = self.create_checkable_items(other, chan)
            channel_children.append(item)

        for child in channel_children:
            self.set_chan_text_colour(child)

    def set_chan_text_colour(self, item):
        if item.text(0)[-1] == "X":
            item.setForeground(0, QtGui.QBrush(QtGui.QColor(200, 55, 70)))
        if item.text(0)[-1] == "Y":
            item.setForeground(0, QtGui.QBrush(QtGui.QColor(43, 175, 78)))
        if item.text(0)[-1] == "Z":
            item.setForeground(0, QtGui.QBrush(QtGui.QColor(85, 120, 198)))

    def create_checkable_items(self, parent, name):
        item = QtWidgets.QTreeWidgetItem(parent)
        item.setFlags(item.flags() | QtCore.Qt.ItemIsTristate | QtCore.Qt.ItemIsUserCheckable)
        item.setText(0, name)
        item.setCheckState(0, QtCore.Qt.Checked)

        return item
      
    def get_all_objects(self):
        self.item_list = []
        self.object_list = []
        for i in range(self.tree_widget.topLevelItemCount()):
            # Note: The Dummy item is included in the count, so there is a "" in the object list
            item = self.tree_widget.topLevelItem(i)
            self.item_list.append(item)
            self.object_list.append(item.text(1))

    def mute_all(self):
        self.get_all_objects()
        attr_list = []
        for item, obj in zip(self.item_list, self.object_list):
            attrs = self.get_checked_attributes(item, obj)
            attr_list.extend(attrs)

        silencer.mute_this(attr_list) # Mutes all checked attrs

        # Press all buttons and highlight
        for obj, btn in self.btn_dic.items():
            item, row, object_name, attrs = self.info_from_btn(btn)

            if item.checkState(0): # Run if All Transforms is checked
                btn.btn1.is_pressed = 0
                self.row_highlight(item, row, btn)

    def unmute_all(self):
        self.get_all_objects()
        self.object_list = list(filter(None, self.object_list))
        attr_list = []

        silencer.unmute_this(self.object_list) # Unmutes all objects

        # Press all buttons and highlight
        for obj, btn in self.btn_dic.items():
            btn.btn1.is_pressed = 1

            item, row, object_name, attrs = self.info_from_btn(btn)
            self.row_highlight(item, row, btn)

    def set_button_press(self, object_name, btn):
        if kh.has_keys(object_name):
            # Check mute status for object
            mute_state = silencer.mute_check(object_name)
            if mute_state: btn.is_pressed = True # Mark button as clicked if object is already muted

            return True
        else:
            return False

    def info_from_btn(self, btn):
        item = self.tree_widget.itemAt(btn.pos())

        # Get the Row index, Find the names in that row, that find the text at the specified column
        row = self.tree_widget.indexOfTopLevelItem(item)
        item = self.tree_widget.topLevelItem(row)
        object_name = item.text(1)

        attrs = self.get_checked_attributes(item, object_name)

        return item, row, object_name, attrs

    def mute_btn_press(self, btn):
        item, row, object_name, attrs = self.info_from_btn(btn)

        if self.set_button_press(object_name, btn):
            self.mute_check_and_execute(btn, attrs)
            self.row_highlight(item, row, btn)

        else: print("No Keys, Skipping")

    def get_checked_attributes(self, item, object_name):
        self.checked_attributes = []

        child_count = item.childCount()
        for i in range(child_count):
            kid = item.child(i)
            kid_text = kid.text(0)

            grandkid_count = kid.childCount()
            for j in range(grandkid_count):
                grandkid = kid.child(j)
                grandkid_text = grandkid.text(0)
                if grandkid.checkState(0) == QtCore.Qt.Checked:
                    # Adding object name to make proper attribute name
                    attribute = object_name + "." + grandkid_text
                    self.checked_attributes.append(attribute)

        return self.checked_attributes

      
    def click_btn_if_muted(self):
        for obj, btn in self.btn_dic.items():
            btn_pos = btn.pos()
            object_name = obj
            item = self.find_item_from_btn(btn)
            # Get the Row index, Find the names in that row, that find the text at the specified column
            row = self.tree_widget.indexOfTopLevelItem(item)

            mute_state = silencer.mute_check(object_name)

            if mute_state:
                btn.is_pressed = True  # Mark button as clicked if object is already muted
                self.row_highlight(item, row, btn)


    def find_item_from_btn(self, btn):
        for i in range(self.tree_widget.topLevelItemCount()):
            item = self.tree_widget.topLevelItem(i)
            maybe_btn = self.tree_widget.itemWidget(item, 2)

            if maybe_btn == btn:
                return item


    def mute_check_and_execute(self, btn, attrs):
        if btn.btn1.is_pressed == False:
            silencer.mute_this(attrs)

        elif btn.btn1.is_pressed == True:
            silencer.unmute_this(attrs)

    def select_object(self):
        objects = []
        selected = self.tree_widget.selectedItems()
        
        if selected:
            for obj in selected:
                object_name = obj.text(1)
                objects.append(object_name)
                
        print(objects)
        silencer.select_object(objects)



if __name__ == "__main__":

    try:
        silence.close()  # pylint: disable=E0601
        silence.deleteLater()
    except:
        pass

    silence = Silencer()
    silence.show()
