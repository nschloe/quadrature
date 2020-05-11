import math

import numpy
import sympy

from ..helpers import article, prod, get_all_exponents
from ._helpers import NSimplexScheme

citation = article(
    authors=["P. Silvester"],
    title="Symmetric quadrature formulae for simplexes",
    journal="Math. Comp.",
    volume="24",
    pages="95-100",
    year="1970",
    url="https://doi.org/10.1090/S0025-5718-1970-0258283-6",
)


def _newton_cotes(dim, n, point_fun):
    degree = n

    # points
    idxs = numpy.array(get_all_exponents(dim + 1, n)[-1])
    points = point_fun(idxs, n)

    # weights
    if n == 0:
        weights = numpy.ones(1)
        return points, weights, degree

    def get_poly(t, m):
        return sympy.prod(
            [
                sympy.poly((t - point_fun(k, n)) / (point_fun(m, n) - point_fun(k, n)))
                for k in range(m)
            ]
        )

    weights = numpy.empty(len(points))
    kk = 0
    for idx in idxs:
        # Define the polynomial which to integrate over the simplex.
        t = sympy.DeferredVector("t")
        g = prod(get_poly(t[k], i) for k, i in enumerate(idx))
        # The integral of monomials over a simplex are well-known, see Silvester.
        weights[kk] = numpy.sum(
            [
                c
                * numpy.prod([math.factorial(l) for l in m])
                * math.factorial(dim)
                / math.factorial(numpy.sum(m) + dim)
                for m, c in zip(g.monoms(), g.coeffs())
            ]
        )
        kk += 1
    return weights, points, degree


def silvester(dim, variant, n):
    # TODO symbolic
    if variant == "closed":
        weights, points, degree = _newton_cotes(dim, n, lambda k, n: k / float(n))
    else:
        assert variant == "open"
        weights, points, degree = _newton_cotes(dim, n, lambda k, n: (k + 1) / float(n + 1 + dim))
        if n == 0:
            degree = 1

    return NSimplexScheme(
        f"Silvester ({variant}, {n})", dim, weights, points, degree, citation
    )