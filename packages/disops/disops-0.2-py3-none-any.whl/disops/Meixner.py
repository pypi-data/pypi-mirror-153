from .OrthogonalPolynomialsGenerator import OrthogonalPolynomialsGenerator

from sympy import poly, rf, Symbol
from math import factorial
from warnings import warn

class Meixner(OrthogonalPolynomialsGenerator):
    """Meixner Polynomials Generator.

    Attributes:
        x (:obj: `sympy.Symbol`): variable of polynomials
        beta (int, float or sympy.Symbol): first parameter of Meixner Polynomials
        c (int, float or sympy.Symbol): second parameter of Meixner Polynomials
    """

    def __init__(self, x, beta, c):
        if not (isinstance(beta, Symbol) or (isinstance(beta, float) and beta > 0)):
            warn("The parameter beta should be a real positive number (float) or a sympy.Symbol.")
        if not (isinstance(c, Symbol) or (isinstance(c, float) and c > 0 and c < 1)):
            warn("The parameter c should be a real number in ]0,1[ (float) or a sympy.Symbol.")
        super().__init__(x, [beta, c])


    def __str__(self):
        return "<Meixner Polynomials Generator of variable "+str(self.x)+" and parameters beta="+str(self.params[0])+", c="+str(self.params[1])+">"


    def _gen_explicit(self, n):
        return poly(sum([rf(-n,k)*rf(-self.x,k)*(1-1/self.params[1])**k/rf(self.params[0],k)/factorial(k) for k in range(n+1)]), self.x)


    def _recurrence_coeffs(self, n):
        return (((self.params[1]-1)*self.x+n-1+(n-1+self.params[0])*self.params[1])/(self.params[1]*(n-1+self.params[0])), (-n+1)/(self.params[1]*(n-1+self.params[0])))