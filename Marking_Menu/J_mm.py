import maya.cmds as mc
import maya.mel as mel
import maya.utils

MENU_NAME = "markingMenu"


class Menu():
    def __init__(self):
        self._removeOld()
        self._build()

    def _removeOld(self):
        if mc.popupMenu(MENU_NAME, ex=1):
            mc.deleteUI(MENU_NAME)

    ### My Functions ###

    def tri_layout(self, *args):
        self.cleanup_my_panels()
        old_model_panels = self.get_visible_modelPanels()

        my_panls_list = []
        mc.frameLayout('TEMP_LAYOUT', visible=0)
        for i, panl in enumerate(old_model_panels):
            my_panl = mc.modelPanel('J_{0}'.format(panl))
            mc.modelPanel(my_panl, e=1, copy=panl)
            my_panls_list.append(my_panl)

        # The Actual Command
        self.delete_graph_editor()  # delete existing graphEditor
        mel.eval('setNamedPanelLayout "tri_graph";')

        new_model_panels = self.get_visible_modelPanels()

        for my_panl, new_panl in zip(my_panls_list, new_model_panels):
            mc.modelPanel(my_panl, e=1, replacePanel=new_panl)
            mc.deleteUI(new_panl, panel=1)

        try:
            mc.deleteUI('TEMP_LAYOUT', layout=1)
        except:
            pass

    def two_dude(self, *args):
        self.cleanup_my_panels()
        old_model_panels = self.get_visible_modelPanels()

        my_panls_list = []
        mc.frameLayout('TEMP_LAYOUT', visible=0)
        for i, panl in enumerate(old_model_panels):
            my_panl = mc.modelPanel('J_{0}'.format(panl))
            mc.modelPanel(my_panl, e=1, copy=panl)
            my_panls_list.append(my_panl)

        # The Actual Command
        mel.eval('setNamedPanelLayout "two_dude";')

        new_model_panels = self.get_visible_modelPanels()

        for my_panl, new_panl in zip(my_panls_list, new_model_panels):
            mc.modelPanel(my_panl, e=1, replacePanel=new_panl)
            mc.deleteUI(new_panl, panel=1)

        mc.deleteUI('TEMP_LAYOUT', layout=1)

    def solo(self, *args):
        # visible_modelPanels = self.get_visible_modelPanels()
        # cam = mc.modelPanel(visible_modelPanels[-1], query=True, camera=True)

        focused_panel = mc.getPanel(withFocus=1)
        cam = mc.modelPanel(focused_panel, q=1, camera=True)

        mel.eval('SingleViewArrangement;')
        mc.lookThru(cam)

    def side_graph(self, *args):
        self.delete_existing_pan("graphEditor")
        mel.eval('setNamedPanelLayout "side_graph";')

    def side_script(self, *args):
        self.delete_existing_pan("scriptEditor")
        mel.eval('setNamedPanelLayout "side_script";')

    def switch_panels(self, *args):
        model_panels = self.get_visible_modelPanels()
        print('{0}, {1}'.format('SWITCH PANELS', model_panels))
        mc.modelPanel(model_panels[0], e=1, replacePanel=model_panels[1])

    def delete_J_panels(self, *args):
        J_pans = [pan for pan in mc.getPanel(all=1) if "J_" in pan]
        if J_pans:
            mc.deleteUI(J_pans)
            print("Deleting: ")
            print(J_pans)

    ### Camera Work ###

    def persp_cam(self, *args):
        cam = "persp"
        self.model_logic(cam)

    def shot_cam(self, *args):
        # Find shot cam
        cam_lyr = mc.ls('cam_lyr', type="displayLayer")  # Find layer

        members = mc.editDisplayLayerMembers(cam_lyr, query=True)  # Get members

        for each in members:
            children = mc.listRelatives(each, ad=1)

            shot_cam = [mc.listRelatives(x, parent=1)[0]
                        for x in children
                        if (mc.ls(x, type="camera") != [])]

            if shot_cam: break

        print('shot cam', shot_cam)
        self.model_logic(shot_cam)  # Look through cam

    ### Helper Functions ###

    def model_logic(self, Camera):
        # To switch the panel to the correct one if it's a non-modelPanel
        focus = mc.getPanel(wf=1)
        visible_panels = mc.getPanel(visiblePanels=1)
        visible_modelPanels = [mod for mod in visible_panels if 'model' in mod]

        # Get modelPanel with persp cam already
        cam_pans = []
        for panelName in mc.getPanel(type="modelPanel"):
            if mc.modelPanel(panelName, query=True, camera=True) == Camera:
                cam_pans.append(panelName)

        # Run if it's not a model panel (i.e. script)
        if 'model' not in focus:

            for i, pan in enumerate(cam_pans):
                # checking the replacement panel will be different (otherwise it'll move around)
                if len(visible_modelPanels) > i:  # Checking length to stop going out of range
                    if visible_modelPanels[i] != pan:
                        print("here")
                        print("pan:", pan)
                        replacement_pan = pan
                        break
            else:  # Make new panel by duplicating visible one
                print("or here")
                new = mc.modelPanel()
                replacement_pan = mc.modelPanel(new, e=1, copy=visible_modelPanels[0])

            mc.modelPanel(replacement_pan, edit=True, replacePanel=focus)
        else:
            mc.lookThru(Camera)
	
    def delete_existing_pan(self, panel_name):
        # Close Panel/Editor if open
        all_panels = mc.getPanel(vis=1)
        panel_obj = [pan for pan in all_panels if panel_name in pan]

        if panel_obj: mc.deleteUI(panel_obj, panel=1)

    def delete_graph_editor(self):
        all_panels = mc.getPanel(all=1)

        for pan in all_panels:
            if 'graphEditor' in pan:
                mc.deleteUI(pan, panel=1)

    def get_visible_modelPanels(self):
        all_model_panels = mc.getPanel(type="modelPanel")
        visible_panels = mc.getPanel(visiblePanels=1)
        visible_modelPanels = [x for x in all_model_panels if x in visible_panels]

        return visible_modelPanels

    def cleanup_my_panels(self):
        model_panels = mc.getPanel(type="modelPanel")
        vis_panels = mc.getPanel(visiblePanels=1)
        invis_model_panels = [x for x in model_panels if x not in vis_panels]
        my_invis_panels = [x for x in invis_model_panels if x[0] == 'J']
        try:
            mc.deleteUI(my_invis_panels, panel=1)
        except:
            pass

    ### build stuff ###
    def _build(self):
        menu = mc.popupMenu(MENU_NAME, mm=1, b=1, aob=1, ctl=1, alt=1, sh=0,
                            p="viewPanes", pmo=1, pmc=self._buildMarkingMenu)

    def _buildMarkingMenu(self, menu, parent):
        ## Radial positioned
        mc.menuItem(p=menu, l="Solo", rp="N", c=self.solo)
        mc.menuItem(p=menu, l="Side Graph", rp="E", c=self.side_graph)
        mc.menuItem(p=menu, l="Tri Graph", rp="S", c=self.tri_layout)
        mc.menuItem(p=menu, l="Two Dude", rp="SE", c=self.two_dude)
        mc.menuItem(p=menu, l="Side Script", rp="W", c=self.side_script)
        mc.menuItem(p=menu, l="Switch Panels", rp="SW", c=self.switch_panels)

        mc.menuItem(p=menu, l="Persp Cam", rp="NE", c=self.persp_cam, image="cameraAim.png")
        mc.menuItem(p=menu, l="Shot Cam", rp="NW", c=self.shot_cam, image="cameraAim.png")

        # subMenu = mc.menuItem(p=menu, l="North Sub Menu", rp="N", subMenu=1)
        # mc.menuItem(p=subMenu, l="North Sub Menu Item 1")
        # mc.menuItem(p=subMenu, l="North Sub Menu Item 2")

        mc.menuItem(p=menu, ob=1, c="print 'South with Options'")

        ## List
        mc.menuItem(p=menu, l="Clear J Panels", c=self.delete_J_panels)



mm = Menu()
