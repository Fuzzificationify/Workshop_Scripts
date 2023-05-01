import maya.cmds as mc
from math import pi

class SecondOrderDynamics:
    def __init__(self, f, z, r, x0):
        self.k1 = z / (pi * f)
        self.k2 = 1 / ((2 * pi * f) * (2 * pi * f))
        self.k3 = r * z / (2 * pi * f)

        self.xp = x0
        self.y = x0
        self.yd = 0

        self.get_input_x()

    def get_input_x(self):
        curve = 'pSphere1_translateX'
        t = [i for i in range(100)]
        self.x_vals = mc.keyframe(curve, q=True, vc=True, t=(t[0], t[-1]))


    def update(self, T, x, xd=None):
        if xd is None:
            xd = (x - self.xp) / T
            self.xp = x

        self.y = self.y + T * self.yd
        self.yd = self.yd + T * (x + self.k3*xd - self.y - self.k1*self.yd) / self.k2

        return self.y

    def run(self):
        for i, x in enumerate(self.x_vals):
            y = self.update(1/25, x)
            print(x, y)
            self.set_keys(y, i)

    def set_keys(self, y, frame):
        mc.setKeyframe('pSphere1_translateY', v=y, t=frame)


dyno = SecondOrderDynamics(3, 0.35, 0, 0)
dyno.run()

