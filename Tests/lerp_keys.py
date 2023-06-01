# Lerp keys from one object to another (I think)

def get_anim_curve(obj, attr):
    attr_name = obj + "." + attr
    anim_curve = mc.keyframe(attr_name, q=1, n=1)

    return anim_curve

def get_input(curv):

    indices = mc.keyframe(curv, q=1, indexValue=1)
    indices = tuple(indices)[0], tuple(indices)[-1]

    vals = mc.keyframe(curv, q=1, index=indices, valueChange=1)
    times = mc.keyframe(curv, q=1, index=indices, timeChange=1)

    return vals, times


def lerp(a, b, t):
    y = a + (b - a)*t
    return y

def spring(p_vals, g_vals, stiffness=7, damping=7):
    dt = 0.01
    q = 0.1

    x = p_vals[0]
    v = (g_vals[0] - x)

    spring_vals = []
    for g in g_vals:

        # v += dt * stiffness * (g - x) + dt * damping * (q - v);
        v += dt * stiffness * (g - x)
        x += dt * v;

        spring_vals.append(x)
    return spring_vals

def lerp_loop(presents, goals, t=0.6):
    lerp_vals = []

    for p_val, g_val in zip(presents, goals):
        lerp_v = lerp(p_val, g_val, t)
        lerp_vals.append(lerp_v)

    return lerp_vals

def spring_loop(presents, goals, t=0.6):

    spring_vals = spring(presents, goals)

    return spring_vals


def set_keys(obj, vals, times):

    for val, time in zip(vals, times):
        mc.setKeyframe(obj, at='tx', value=val, time=time)


def main(present_obj, goal_obj):

    present_curv = get_anim_curve(present_obj, 'tx')
    goal_curv = get_anim_curve(goal_obj, 'tx')


    pres_vals, pres_times = get_input(present_curv)
    goal_vals, goal_times = get_input(goal_curv)

    lerp_vals = spring_loop(pres_vals, goal_vals)

    set_keys(present_obj, lerp_vals, pres_times)


present_obj = 'pCube1'
goal_obj = 'pSphere1'
main(present_obj, goal_obj)
