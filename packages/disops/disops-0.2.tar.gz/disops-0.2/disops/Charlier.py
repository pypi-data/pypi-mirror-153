from .OrthogonalPolynomialsGenerator import OrthogonalPolynomialsGenerator

from sympy import poly, Symbol
from math import prod, comb
from warnings import warn

class Charlier(OrthogonalPolynomialsGenerator):
    """Charlier Polynomials Generator.

    Attributes:
        x (:obj: `sympy.Symbol`): variable of polynomials
        mu (int, float or sympy.Symbol): parameter of Chalier Polynomials
    """

    def __init__(self, x, mu):
        if not (isinstance(mu, Symbol) or (isinstance(mu, float) and mu > 0)):
            warn("The parameter mu should be a real positive number (float) or a sympy.Symbol.")
        super().__init__(x, [mu])


    def __str__(self):
        return "<Chalier Polynomials Generator of variable "+str(self.x)+" and parameter mu="+str(self.params[0])+">"


    def _gen_explicit(self, n):
        return poly(sum([ comb(n, k)*prod([self.x-k+1+i for i in range(k)])*(-self.params[0])**(n-k) for k in range(n+1)]), self.x)


    def _recurrence_coeffs(self, n):
        return (self.x-n+1-self.params[0], -self.params[0]*(n-1))