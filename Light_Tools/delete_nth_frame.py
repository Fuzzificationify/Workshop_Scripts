keys = mc.keyframe(q=1, n=1)

for i in range(1063, 1170):
    if (i+2) % 4 != 0:
        mc.cutKey(keys, time=(i,))
