minTime = mc.playbackOptions(q=1, minTime=1)
maxTime = mc.playbackOptions(q=1, maxTime=1)
time_range = minTime, maxTime


fk_ctrls = mc.ls(sl=1)
jnt_list = []
circ_list = []
constraints = []
cluster_list = []

mc.select(cl=1)

for i, ctrl in enumerate(fk_ctrls):
    
    jnt = mc.joint(n='jnt_{0}'.format(i))    
    pCon = mc.parentConstraint(fk_ctrls[i], jnt)[0]
    constraints.append(pCon)
    jnt_list.append(jnt)
    

    
mc.bakeResults(jnt_list, time=time_range)

mc.select(jnt_list[0], jnt_list[-1])
ikHand, effectr, curv = mc.ikHandle(solver="ikSplineSolver", simplifyCurve=0)

curv_cvs = mc.ls(curv + '.cv[:]', flatten=1)
mc.delete(curv_cvs[1] ,curv_cvs[-2])

# Group Clusters
grp_size = 2
curv_cvs_grpd = [curv_cvs[i:i+grp_size] for i in range(0, len(curv_cvs), grp_size)]

# Clusters
for cv in curv_cvs_grpd:
    
    clustr = mc.cluster(cv)[1]
    cluster_list.append(clustr)

mc.group(name="clusters", empty=1)
mc.parent(cluster_list, "clusters")

# Make Circles
for i, ctrl in enumerate(curv_cvs_grpd): 
    circ = mc.circle(ch=0)[0]
    pCon2 = mc.parentConstraint(cluster_list[i], circ)[0]
    constraints.append(pCon2)
    circ_list.append(circ)


# Contraining the Cluster to Circles
for i, ctrl in enumerate(cluster_list):
    pCon = mc.parentConstraint(circ_list[i], cluster_list[i], mo=1)
  
mc.bakeResults(circ_list, time=time_range)
mc.delete(constraints)

# Constraining the FK Controls
for i, ctrl in enumerate(fk_ctrls):
    mc.orientConstraint(jnt_list[i], fk_ctrls[i])
