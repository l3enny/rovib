from math import exp
import spectrum

def lines(istate, vi, fstate, vf, Jmax, Tr):
    origin = istate.E(vi) - fstate.E(vf)

    Bx = 1.9898         # 1/cm
    h = 6.62606957e-27  # erg.sec
    c = 2.99792458e10   # cm/sec
    k = 1.3806488e-16   # erg/K
    def f(j):
        return (2 * j + 1) * exp(-j * (j + 1) * (h * c * Bx) / (k * Tr))
    Qnorm = sum([f(j) for j in range(Jmax)])
    
    # Initialize different branches, and their triplet splittings.
    P = {0: {}, 1: {}, 2: {}}
    Q = {1: {}, 2: {}}
    R = {0: {}, 1: {}, 2: {}}
    wavelengths = (P, Q, R)
    spec = spectrum.Spectrum()
    for J in range(Jmax+1):
        # P branch calculations
        for O in range(3):
            if J - 1 < O or J < O:
                pass
            else:
                shift = F(istate, vi, J - 1, O) - F(fstate, vf, J, O)
                wavelength = 1 / (100 * (origin + shift))
                wavelengths[0][O][J] = wavelength
                S = (J + O) * (J - O) / J
                I = S / Qnorm * exp(-J * (J - 1) * (h * c * Bx) / (k * Tr))
                spec[wavelength] = I
                
        # Q branch calculations
        for O in range(1,3):
            if J < O:
                pass
            else:
                shift = F(istate, vi, J, O) - F(fstate, vf, J, O)
                wavelength = 1 / (100 * (origin + shift))
                wavelengths[1][O][J] = wavelength
                S = (2 * J + 1) * O * O / J
                I = S / Qnorm * exp(-J * (J + 1) * (h * c * Bx) / (k * Tr))
                spec[wavelength] = I

        # R branch calculations
        for O in range(3):
            if J + 1 < O or J < O or J is 0:
                pass
            else:
                shift = F(istate, vi, J + 1, O) - F(fstate, vf, J, O)
                wavelength = 1 / (100 * (origin + shift))
                wavelengths[2][O][J] = wavelength
                S = (J + O) * (J - O) / J
                I = S / Qnorm * exp(-J * (J + 1) * (h * c * Bx) / (k * Tr))
                spec[wavelength] = I
    return spec

def F(state, v, J, O):
    B = state.B
    D = state.D
    Z1, Z2 = Z(state, v, J)
    if O is 0:
        return B(v) * (J * (J + 1) - Z1**0.5 - 2.0 * Z2) - D(v) * (J - 0.5)**4
    elif O is 1:
        return B(v) * (J * (J + 1) + 4 * Z2) - D(v) * (J + 0.5)**4
    elif O is 2:
        return B(v) * (J * (J + 1) + Z1**0.5 - 2.0 * Z2) - D(v) * (J + 1.5)**4
    else:
        raise ValueError('Omega was %d but can only be 0, 1 or 2' % O)

def Z(state, v, J):
    Y = state.Y
    Z1 = Y(v) * (Y(v) - 4) + (4.0 / 3.0) + 4 * J * (J + 1)
    Z2 = 1.0 / (3 * Z1) * (Y(v) * (Y(v) - 1) - (4.0 / 9.0) - 2 * J * (J + 1))
    return Z1, Z2

