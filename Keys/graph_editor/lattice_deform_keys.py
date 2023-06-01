# 3 x 3 Lattice

if mc.contextInfo("latticeKeyDeform1", exists=1):

	mc.latticeDeformKeyCtx("latticeKeyDeform1", e=1, latticeColumns=3, latticeRows=3)
	mc.setToolTo("latticeKeyDeform1")

else:
	mc.latticeDeformKeyCtx("latticeKeyDeform1", latticeColumns=3, latticeRows=3)
	mc.setToolTo("latticeKeyDeform1")
    
    
    
# 5 x 5 Lattice

if mc.contextInfo("latticeKeyDeform1", exists=1):

	mc.latticeDeformKeyCtx("latticeKeyDeform1", e=1, latticeColumns=5, latticeRows=5)
	mc.setToolTo("latticeKeyDeform1")

else:
	mc.latticeDeformKeyCtx("latticeKeyDeform1", latticeColumns=5, latticeRows=5)
	mc.setToolTo("latticeKeyDeform1")
