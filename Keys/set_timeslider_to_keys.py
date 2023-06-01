import pymel.core as pm
from Helper_Functions import keyframe_helpers as kh

def get_timeslider_snapshot():
    min_playback, max_playback = kh.get_scene_range()
    min_anim, max_anim = kh.get_minmax_scene_range()

    return [min_playback, max_playback], [min_anim, max_anim]

def get_keyframe_times(sel):
    # Get lowest and highest times from selection
    times_list = []

    for obj in sel:
        start_time, end_time, _ = kh.get_key_times(obj, sl_keys=False)
        times_list.append(start_time)
        times_list.append(end_time)

    key_times = [min(times_list), max(times_list)]
    return key_times

def set_slider_to_keys(key_times):
    mc.playbackOptions(min=key_times[0], max=key_times[1])

def set_slider_to_snapshot(snapshot):
    playback = snapshot[0]
    anim =  snapshot[1]
    mc.playbackOptions(min=playback[0], max=playback[1], animationStartTime=anim[0], animationEndTime=anim[1])



def to_keyframes(sel):
    key_times = get_keyframe_times(sel)
    set_slider_to_keys(key_times)

    return key_times

def to_snapshot(snapshot):
    set_slider_to_snapshot(snapshot)

def main():

    sel = mc.ls(sl=1)
    time_snapshot = get_timeslider_snapshot()

    key_times = to_keyframes(sel)

    return key_times, time_snapshot



try:
    key_times
except NameError:
    key_times = None

try:
    time_snapshot
except NameError:
    time_snapshot = None


scene_times = get_timeslider_snapshot()[0]

if scene_times == key_times:
    if time_snapshot != None:
        to_snapshot(time_snapshot)

else:
    key_times, time_snapshot = main()
