import maya.cmds as mc

riv = 'rivet_loc'
target = 'rivet_keyed'
anim_layer = 'rivet_offset'

mc.animLayer(anim_layer, e=1, mute=1, lock=1)
p_con = mc.pointConstraint(riv, target)

my_bake(target)
print("working?")
mc.delete(p_con)
mc.animLayer(anim_layer, e=1, mute=0, lock=0)

def my_bake(obj):
    # Get Time Slider Range
    minTime = mc.playbackOptions(q=1, minTime=1)
    maxTime = mc.playbackOptions(q=1, maxTime=1)

    timeSliderRange = minTime, maxTime

    # Bake
    mc.bakeResults(obj, t=timeSliderRange)

    # Delete Constraint
    #child_con = mc.listRelatives(obj, children=1, type='constraint')
    #mc.delete(child_con, constraints=1)
