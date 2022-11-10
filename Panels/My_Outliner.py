import maya.cmds as cmds

bob = cmds.getPanel(vis=1)

try:
    panel
except NameError:
    panel = None

# delete outliner from scene if it's been dragged off and closed
if cmds.window("myOutliner", exists=1):
    cmds.deleteUI("myOutliner")


if panel in cmds.getPanel(vis=1):
    Yup = "Yep"
    cmds.deleteUI(myDoc)

else:
    # Create a new regular outliner in its own window

    myWin = cmds.window(height=100, width=500)
    #cmds.showWindow(myWin)

    cmds.frameLayout( labelVisible=False )
    panel = cmds.outlinerPanel()
    outliner = cmds.outlinerPanel(panel, query=True,outlinerEditor=True)
    cmds.outlinerEditor( outliner, edit=True, mainListConnection='worldList',
    selectionConnection='modelList', showShapes=False, showReferenceNodes=False, showReferenceMembers=False, showAttributes=False, showConnected=False, showAnimCurvesOnly=False, autoExpand=False, showDagOnly=True, ignoreDagHierarchy=False, expandConnections=False, showNamespace=True, showCompounds=True, showNumericAttrsOnly=False, highlightActive=True, autoSelectNewObjects=False, doNotSelectNewObjects=False, transmitFilters=False, showSetMembers=True, setFilter='defaultSetFilter', ignoreHiddenAttribute=False, ignoreOutlinerColor=False )
    #cmds.showWindow()
    myDoc = "myOutliner"

    cmds.dockControl(myDoc,
                     allowedArea = ["left","right"],
                     area = "left",
                     width=600,
                     content = myWin,
                     floating = False)
