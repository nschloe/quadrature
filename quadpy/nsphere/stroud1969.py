# -*- coding: utf-8 -*-
#
from __future__ import division
import math
import numpy

from ..helpers import untangle, pm, fsd2
from .helpers import integrate_monomial_over_unit_nsphere


class Stroud1969(object):
    '''
    A.H. Stroud,
    A Fifth Degree Integration Formula for the n-Simplex,
    SIAM J. Numer. Anal., 6(1), 90–98. (9 pages),
    <https://doi.org/10.1137/0706009>.
    '''
    # pylint: disable=too-many-locals
    def __init__(self, n):
        assert 3 <= n <= 16

        self.dim = n
        self.degree = 11

        plus_minus = numpy.array([+1, -1])
        sqrt3 = math.sqrt(3.0)

        t = math.sqrt(1.0 / n)
        r1, r2 = numpy.sqrt(
                (n + 6 - plus_minus*4*sqrt3) / (n**2 + 12*n - 12)
                )
        s1, s2 = numpy.sqrt(
                (7*n - 6 + plus_minus*4*(n-1)*sqrt3) / (n**2 + 12*n - 12)
                )
        u1, u2 = numpy.sqrt(
                (n + 12 + plus_minus*8*sqrt3) / (n**2 + 24*n - 48)
                )
        v1, v2 = numpy.sqrt(
                (7*n - 12 - plus_minus*4*(n-2)*sqrt3) / (n**2 + 24*n - 48)
                )

        A = {
            3: 9.0 / 70.0,
            4: 7.0 / 135.0,
            5: 0.211979378646e-1,
            6: 0.281250000000,
            7: 0.111934731935e+1,
            8: 0.282751322751e+1,
            9: 0.568266145619e+1,
            10: 0.993785824515e+1,
            11: 0.158196616478e+2,
            12: 0.235285714285e+2,
            13: 0.332409299392e+2,
            14: 0.451113811729e+2,
            15: 0.592754264177e+2,
            16: 0.758518518518e+2,
            }
        B1 = {
            3: (122.0 + 9 * math.sqrt(3.0)) / 6720 * 8,
            4: 0.967270533860e-1,
            5: 0.638253880175e-1,
            6: 0.452340041459e-1,
            7: 0.337329118818e-1,
            8: 0.261275095270e-1,
            9: 0.208331595340e-1,
            10: 0.169937111647e-1,
            11: 0.141147212492e-1,
            12: 0.118949128383e-1,
            13: 0.101424250926e-1,
            14: 0.873046796644e-2,
            15: 0.757257014768e-2,
            16: 0.660813369775e-2,
            }
        B2 = {
            3: (122.0 - 9 * math.sqrt(3.0)) / 6720 * 8,
            4: 0.514210947621e-1,
            5: +0.213579471658e-1,
            6: -0.108726067638,
            7: -0.371589499738,
            8: -0.786048144448,
            9: +0.136034060198e+1,
            10: +0.209547695631e+1,
            11: +0.298784764467e+1,
            12: +0.403107480702e+1,
            13: +0.521726499521e+1,
            14: +0.653783099707e+1,
            15: +0.798401677102e+1,
            16: +0.954722261180e+1,
            }
        C1 = {
            4: 0.592592592592e-1,
            5: 0.236639091329e-1,
            6: 0.525940190875e-1,
            7: 0.925052768546e-1,
            8: 0.141316953438,
            9: 0.196818580052,
            10: 0.257027634179,
            11: 0.320299222258,
            12: 0.385326226441,
            13: 0.451098131789,
            14: 0.516849445559,
            15: 0.582010515746,
            16: 0.646165210110,
            }
        C2 = {
            5: 0.316246294890e-1,
            6: 0.207194729760e-1,
            7: 0.144303800811e-1,
            8: 0.105348984135e-1,
            9: 0.798435122193e-2,
            10: 0.623845929545e-2,
            11: 0.499896882962e-2,
            12: 0.409176297655e-2,
            13: 0.341037426698e-2,
            14: 0.288710646943e-2,
            15: 0.247745182907e-2,
            16: 0.215128820597e-2,
            }

        data = [
            (A[n], pm(n, t)),
            (B1[n], fsd2(n, s1, r1, 1, n-1)),
            (B2[n], fsd2(n, s2, r2, 1, n-1)),
            ]
        if n >= 4:
            data += [
                (C1[n], fsd2(n, v1, u1, 2, n-2))
                ]
        if n >= 5:
            data += [
                (C2[n], fsd2(n, v2, u2, 2, n-2))
                ]

        self.points, self.weights = untangle(data)
        self.weights *= integrate_monomial_over_unit_nsphere(n * [0])
        self.weights /= 2.0**n

        return
