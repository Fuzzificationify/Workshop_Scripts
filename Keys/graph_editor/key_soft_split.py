# Sets and deletes keys based on average value between
# Select a few keys, and it will split 1 into 2, 2 into 3.
# Or reduce 3 to 2, 2 to 1

import pymel.core as pm

def average(lst):
    return sum(lst) / len(lst)

def negative_split():
    curv = pm.PyNode(pm.keyframe(q=1, n=1)[0])
    key_list = pm.keyframe(q=1, selected=True)
    new_key_times = []

    for i in range(len(key_list)-1):

        mid_time = (key_list[i] + key_list[i+1]) / 2
        mid_val = curv.evaluate(mid_time)
        pm.setKeyframe(curv, time=mid_time, value=mid_val)

        new_key_times.append(mid_time)

    pm.cutKey(selectKey=1)
    pm.selectKey(clear=1) # SnapKey only works with no selection
    pm.snapKey( t=(new_key_times[0], new_key_times[-1]) )
    pm.selectKey(curv, time=(new_key_times[0], new_key_times[-1]))


def positive_split():
    curv = pm.PyNode(pm.keyframe(q=1, n=1)[0])
    slkey_tm = pm.keyframe(q=1, selected=True)

    for k in slkey_tm:
        if k == slkey_tm[0]:
            down = curv.evaluate(k - 1)
            pm.setKeyframe(curv, time=k - 1, value=down)
        if k == slkey_tm[-1]:
            up = curv.evaluate(k + 1)
            pm.setKeyframe(curv, time=k + 1, value=up)


    if len(slkey_tm) > 1:
        mean_tm = average(slkey_tm)
        print(mean_tm)
        mid_val = curv.evaluate(mean_tm)
        pm.setKeyframe(curv, time=mean_tm, value=mid_val)

    pm.cutKey(curv, time=(slkey_tm[0], ))
    pm.cutKey(curv, time=(slkey_tm[-1], ))

    pm.selectKey(curv, time=(slkey_tm[0]-1,slkey_tm[-1]+1))

