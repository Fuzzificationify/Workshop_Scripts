mc.selectType(animCurve=True)
mc.optionVar(intValue=['curveSelectionOn', 1])


mc.selectType(animCurve=False)
mc.optionVar(intValue=['curveSelectionOn', 0])


# Toggle Only Curves vs Everything Else
if mc.selectType(q=1, animCurve=True):
    mc.selectType(animCurve=False, animKeyframe=True, animBreakdown=True, animInTangent=True, animOutTangent=True)

else:
    mc.selectType(animCurve=True, animKeyframe=False, animBreakdown=False, animInTangent=False, animOutTangent=False)
    
 
 # Turn on everything
 mc.selectType(animCurve=True, animKeyframe=True, animBreakdown=True, animInTangent=True, animOutTangent=True)
