import maya.cmds as mc

obj = mc.ls(sl=1)
name = mc.keyframe(obj, q=1, n=1, sl=1)
keys = mc.keyframe(obj, q=1, sl=1, indexValue=1)

vals = mc.keyframe(name, q=1, sl=1, valueChange=1)



for i, key in enumerate(keys):

    oval = vals[i-1] * 1.1
    nval = vals[i+1] * 1.1
    wop = (oval + nval) / 2
    cval = vals[i] * 1.2 - wop

    mc.keyframe(name, e=1, index=(key, key), relative=1, valueChange=cval)







import maya.cmds as mc

obj = mc.ls(sl=1)
name = mc.keyframe(obj, q=1, n=1, sl=1)
keys = mc.keyframe(obj, q=1, sl=1, indexValue=1)

vals = mc.keyframe(name, q=1, sl=1, valueChange=1)


mid = (len(keys) - 1) / 2

for i, key in enumerate(keys):


    if i > mid:
        n = vals[i]
        dif = mid - i
        mirror_i = mid + dif
        mirror_val = vals[mirror_i]

        mc.keyframe(name, e=1, index=(key, key), relative=0, valueChange=mirror_val)






import maya.cmds as mc

obj = mc.ls(sl=1)
name = mc.keyframe(obj, q=1, n=1, sl=1)
keys = mc.keyframe(obj, q=1, sl=1, indexValue=1)

vals = mc.keyframe(name, q=1, sl=1, valueChange=1)


mid = (len(keys) - 1) / 2
mid_val = vals[mid]

for i, key in enumerate(keys):


    n = vals[i]
    dis = abs(mid - i)

    nval = vals[i] / dis


    mc.keyframe(name, e=1, index=(key, key), relative=0, valueChange=nval)






import maya.cmds as mc

obj = mc.ls(sl=1)
name = mc.keyframe(obj, q=1, n=1, sl=1)
keys = mc.keyframe(obj, q=1, sl=1, indexValue=1)

vals = mc.keyframe(name, q=1, sl=1, valueChange=1)
norm_vals = [float(i)/max(vals) for i in vals]
vals = norm_vals

mid = (len(keys) - 1) / 2
mid_val = vals[mid]

for i, key in enumerate(keys):

    n = vals[i]
    dis = abs(mid - i)

    nval = abs(dis*(vals[i] * dis))*.01


    mc.keyframe(name, e=1, index=(key, key), relative=1, valueChange=nval)





import maya.cmds as mc

obj = mc.ls(sl=1)
name = mc.keyframe(obj, q=1, n=1, sl=1)
keys = mc.keyframe(obj, q=1, sl=1, indexValue=1)

vals = mc.keyframe(name, q=1, sl=1, valueChange=1)
#norm_vals = [float(i)/max(vals) for i in vals]
#vals = norm_vals

mid = (len(keys) - 1) / 2
mid_val = vals[mid]
print("mid val is:", mid_val)

for i, key in enumerate(keys):

    dis = abs(mid - i)

    #nval = abs(dis*(vals[i] * dis))*.4
    nval = vals[i] + (dis*.1)
    print("nval is:", nval)
    if nval > mid_val:
        #print("YEP")
        nval = mid_val
        mc.keyframe(name, e=1, index=(key, key), relative=0, valueChange=mid_val)

    else:
        #print("NOP")
        mc.keyframe(name, e=1, index=(key, key), relative=0, valueChange=nval)







import maya.cmds as mc

obj = mc.ls(sl=1)
name = mc.keyframe(obj, q=1, n=1, sl=1)
keys = mc.keyframe(obj, q=1, sl=1, indexValue=1)

vals = mc.keyframe(name, q=1, sl=1, valueChange=1)

#norm_vals = [float(i)/max(vals) for i in vals]
#vals = norm_vals

high = max(vals)
high_index = vals.index(high)

mid = (len(keys) - 1) / 2
mid_val = vals[mid]


for i, key in enumerate(keys):

    dis = abs(high_index - i)

    nval = vals[i] + (dis*.1)

    if i == 0 or key == keys[-1]:
        print("nval is:", nval)
        nval = abs(nval *.1)
        print("new nval is:", nval)
        mc.keyframe(name, e=1, index=(key, key), relative=1, valueChange=nval)

    elif nval > high:
        #print("YEP")
        nval = mid_val
        mc.keyframe(name, e=1, index=(key, key), relative=0, valueChange=high)

    else:
        #print("NOP")
        mc.keyframe(name, e=1, index=(key, key), relative=0, valueChange=nval)
