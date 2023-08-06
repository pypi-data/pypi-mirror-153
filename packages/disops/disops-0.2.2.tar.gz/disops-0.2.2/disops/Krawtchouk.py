from .OrthogonalPolynomialsGenerator import OrthogonalPolynomialsGenerator

from sympy import poly, rf, Symbol
from math import factorial
from warnings import warn

class Krawtchouk(OrthogonalPolynomialsGenerator):
    """Krawtchouk Polynomials Generator.

    Attributes:
        x (:obj: `sympy.Symbol`): variable of polynomials
        N (int): size of Krawtchouk Polynomials Sequence
        p (float or sympy.Symbol): parameter of Krawtchouk polynomials
    """

    def __init__(self, x, N, p):
        if not (isinstance(N, int) and N > 0):
            warn("The size N should be an integer positive number (int).")
        if not (isinstance(p, Symbol) or (isinstance(p, float) and p > 0 and p < 1)):
            warn("The parameter p should be a real number in ]0,1[ (float) or a sympy.Symbol.")
        super().__init__(x, [N, p])


    def __str__(self):
        return "<Krawtchouk Polynomials Generator of variable "+str(self.x)+", size="+str(self.params[0])+" and parameter p="+str(self.params[1])+">"


    def _gen_explicit(self, n):
        return poly(sum([rf(-n, k) * rf(-self.x, k) / rf(-self.params[0], k) / factorial(k) * self.params[1]**(-k) for k in range(n+1)]), self.x)


    def _recurrence_coeffs(self, n):
        return ((-self.x + self.params[1]*(self.params[0]-n+1) + (n-1)*(1-self.params[1]))/(self.params[1]*(self.params[0]-n+1)), -(n-1)*(1-self.params[1])/(self.params[1]*(self.params[0]-n+1)))