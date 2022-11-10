import maya.cmds as mc

selObj = mc.ls(sl=1)

# Get Time Slider Range
minTime = mc.playbackOptions(q=1, minTime=1)
maxTime = mc.playbackOptions(q=1, maxTime=1)

timeSliderRange = minTime, maxTime

# Bake
mc.bakeResults(selObj, t=timeSliderRange)

# Delete Constraint
child_con = mc.listRelatives(selObj, children=1, type='constraint')
mc.delete(child_con, constraints=1)
