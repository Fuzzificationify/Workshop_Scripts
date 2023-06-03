#Tent copier

source = mc.select("chrGiantOctopus01A_13009_0:l_tentalceA_layerA")
source = mc.ls(sl=1)
mc.copyKey(source, attribute='r')

mc.select("chrGiantOctopus01A_13009_0:r_tentalceA_layerA")
ra = mc.ls(sl=1)
mc.select("chrGiantOctopus01A_13009_0:l_tentalceB_layerA")
lb = mc.ls(sl=1)
mc.select("chrGiantOctopus01A_13009_0:l_tentalceC_layerA")
lc = mc.ls(sl=1)
mc.select("chrGiantOctopus01A_13009_0:l_tentalceD_layerA")
ld = mc.ls(sl=1)
mc.select("chrGiantOctopus01A_13009_0:r_tentalceB_layerA")
rb = mc.ls(sl=1)
mc.select("chrGiantOctopus01A_13009_0:r_tentalceC_layerA")
rc = mc.ls(sl=1)
mc.select("chrGiantOctopus01A_13009_0:r_tentalceD_layerA")
rd = mc.ls(sl=1)

tent_list = [ra, lb, lc, ld, rb, rc, rd]

for tent in tent_list:
    mc.pasteKey(tent)
