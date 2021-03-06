from math import pi

import numpy as np

from ..helpers import QuadratureScheme, backend_to_function, expand_symmetries

schemes = {}


def register(in_schemes):
    for scheme in in_schemes:
        schemes[scheme.__name__] = scheme


class E3rScheme(QuadratureScheme):
    def __init__(self, name, symmetry_data, degree, source, tol=1.0e-14):
        self.symmetry_data = symmetry_data
        points, weights = expand_symmetries(symmetry_data, dim=3)
        self.domain = "E3r"
        super().__init__(name, weights, points, degree, source, tol)

    def integrate(self, f, dot=np.dot):
        flt = np.vectorize(float)
        ref_vol = 8 * pi
        return ref_vol * dot(f(flt(self.points)), flt(self.weights))

    def show(self, backend="vtk"):
        """Displays scheme for E_3^r quadrature."""
        backend_to_function[backend](
            self.points, self.weights, volume=8 * np.pi, edges=[]
        )


def get_good_scheme(degree):
    if degree <= 7:
        return {
            0: schemes["stroud_secrest_08"],
            1: schemes["stroud_secrest_08"],
            2: schemes["stroud_secrest_08"],
            3: schemes["stroud_secrest_08"],
            4: schemes["stroud_secrest_08"],
            5: schemes["stroud_secrest_08"],
            6: schemes["stroud_secrest_10"],
            7: schemes["stroud_secrest_10"],
        }[degree]()
    return None
