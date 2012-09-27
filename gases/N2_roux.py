# All values calculated from constants provided by Roux, Michaud and Vervloet

class B3Pig(object):

    def E(self, v):
        T0 = 59306.8
        w  = 1734.022
        wx = 14.410
        wy = -0.0045
        wz = -0.00043
        Te = T0 - (w / 2) + (wx / 4) - (wy / 8) - (wz / 16)
        return Te + w * (v + 0.5) - wx * (v + 0.5)**2 + wy * (v + 0.5)**3 \
               + wz * (v + 0.5)**4

    def B(self, v):
        Be = 1.63769
        aB = 0.1786
        BB = -0.00014
        gB = 0.000010
        dB = -0.000004
        return Be - aB * (v + 0.5) + BB * (v + 0.5)**2 + gB * (v + 0.5)**3 \
               + dB * (v + 0.5)**4

    def Y(self, v):
        A = 42.256
        return A / self.B(v)

    def D(self, v):
        Be = 1.63769
        w  = 1734.022
        wx = 14.410
        a = 0.1786
        De = 4 * Be**3 / w**2
        Beta = De * ((8 * wx / w) - (5 * a / Be) - (a**2 * w / (24 * Be**3)))
        return De + Beta * (v + 1/2)

class C3Piu(object):
    
    def E(self, v):
        T0 = 88977.9
        w = 2047.7928
        wx = 28.9421
        wy = 2.24537
        wz = -5.51196e-1
        Te = T0 - (w / 2) + (wx / 4) - (wy / 8) - (wz / 16)
        return Te + w * (v + 0.5) - wx * (v + 0.5)**2 + wy * (v + 0.5)**3 \
               + wz * (v + 0.5)**4

    def B(self, v):
        Be = 1.8268
        aB = 0.024
        BB = 0.0019
        gB = -0.0006
        return Be - aB * (v + 0.5) + BB * (v + 0.5)**2 + gB * (v + 0.5)**3
    
    def Y(self, v):
        A = 39.5
        return A / self.B(v)

    def D(self, v):
        Be = 1.8268
        w  = 2047.7928
        wx = 28.9421
        a = 0.24
        De = 4 * Be**3 / w**2
        Beta = De * ((8 * wx / w) - (5 * a / Be) - (a**2 * w / (24 * Be**3)))
        return De + Beta * (v + 1/2)
