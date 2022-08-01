import maya.cmds as cmds

#
#Define a procedure that returns a value to be used by the Heads Up Display
#
def objectPosition(*args):
        try:
                selectedNodes = cmds.selectedNodes()
                mainObj = selectedNodes[-1]
                positionList = cmds.getAttr('%s.translate' % mainObj)
                return positionList[0]
        except:
                return (0.0,0.0,0.0)


def get_stretch():
    stretch = cmds.getAttr('hatzegopteryxAvA0001:rp:head_CTRL.stretchValueDisplay')
    return stretch
#
#Now, create a HUD object to display the return value of the above procedure
#
#Attributes:
#
#        - Section 1, block 0, represents the top second slot of the view.
#        - Set the blockSize to "medium", instead of the default "small"
#        - Assigned the HUD the label: "Position"
#        - Defined the label font size to be large
#        - Assigned the HUD a command to run on a SelectionChanged trigger
#        - Attached the attributeChange node change to the SelectionChanged trigger
#          to allow the update of the data on attribute changes.
#
cmds.headsUpDisplay( 'HUDObjectPosition', section=1, block=0, blockSize='medium', label='Position', labelFontSize='large', command=get_stretch, event='timeChanged')

#cmds.headsUpDisplay( 'HUDObjectPosition', rem=True )

#cmds.headsUpDisplay(le=1)
