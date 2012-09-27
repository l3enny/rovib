# All values calculated from constants provided by Laher and Gilmore's 1990
# paper on improved fits for molecular nitrogen spectra

class B3Pig(object):

    def E(self, v):
        T0 = 59306.8
        w  = 1734.38
        wx = 14.558
        wy = 1.397e-2
        wz = -1.127e-3
        Te = T0 - (w / 2) + (wx / 4) - (wy / 8) - (wz / 16)
        return Te + w * (v + 0.5) - wx * (v + 0.5)**2 + wy * (v + 0.5)**3 \
               + wz * (v + 0.5)**4

    def B(self, v):
        Be = 1.63802
        a = 1.8302e-2
        g = -8.36e-6
        d = -3.39e-6
        return Be - a * (v + 0.5) + g * (v + 0.5)**2 + d * (v + 0.5)**3

    def Y(self, v):
        A = 42.24
        return A / self.B(v)

    def D(self, v):
        Be = 1.63802
        w  = 1734.38
        wx = 14.558
        a = 1.8302e-2
        De = 4 * Be**3 / w**2
        Beta = De * ((8 * wx / w) - (5 * a / Be) - (a**2 * w / (24 * Be**3)))
        return De + Beta * (v + 1/2)

class C3Piu(object):
    
    def E(self, v):
        T0 = 88977.9
        w = 2047.17
        wx = 28.445
        wy = 2.0883
        wz = -5.350e-1
        Te = T0 - (w / 2) + (wx / 4) - (wy / 8) - (wz / 16)
        return Te + w * (v + 0.5) - wx * (v + 0.5)**2 + wy * (v + 0.5)**3 \
               + wz * (v + 0.5)**4

    def B(self, v):
        Be = 1.8247
        a = 1.868e-2
        g = -2.28e-3
        d = 7.33e-4
        e = -1.5e-4
        return Be - a * (v + 0.5) + g * (v + 0.5)**2 + d * (v + 0.5)**3 \
               + e * (v + 0.5)**4
    
    def Y(self, v):
        A = 39.2
        return A / self.B(v)

    def D(self, v):
        Be = 1.8247
        w  = 2047.17
        wx = 28.445
        a = 1.868e-2
        De = 4 * Be**3 / w**2
        Beta = De * ((8 * wx / w) - (5 * a / Be) - (a**2 * w / (24 * Be**3)))
        return De + Beta * (v + 1/2)
