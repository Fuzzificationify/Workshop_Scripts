import pymel.core as pm
import random

dogs = pm.ls(sl=1)
ctrl_name = "ctrl_m_headFkSub"
ctrl_list = []

for dog in dogs:
    name_space = dog.namespace()
    ctrl_list.append(name_space + ctrl_name)

pm.select(ctrl_list)



# Select global
import pymel.core as pm

sel = pm.ls(sl=1)[0]
name_space = sel.namespace()

global_ctrl = name_space + "ctrl_m_world"
pm.select(global_ctrl)



import pymel.core as pm

dogs = pm.ls(sl=1)
raw_ctrl_sel = [u'chrWartDog01A_16016_1:ctrl_m_tailFkSplineA',
 u'chrWartDog01A_16016_1:ctrl_m_tailFkSplineB',
 u'chrWartDog01A_16016_1:ctrl_m_tailFkSplineC',
 u'chrWartDog01A_16016_1:ctrl_m_tailFkSplineD',
 u'chrWartDog01A_16016_1:ctrl_m_tailFkSplineE',
 u'chrWartDog01A_16016_1:ctrl_m_tailFkSplineF',
 u'chrWartDog01A_16016_1:ctrl_m_tailFkSplineG']

ctrl_set = [x.rpartition(':')[-1] for x in raw_ctrl_sel]
ctrl_list = []

for dog in dogs:
    name_space = dog.namespace()

    for ctrl_name in ctrl_set:
        ctrl_list.append(name_space + ctrl_name)

pm.select(ctrl_list)
