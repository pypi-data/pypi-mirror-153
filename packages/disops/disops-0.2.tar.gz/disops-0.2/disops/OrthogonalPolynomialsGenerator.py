from sympy import poly, degree, LC, monic
from sympy.plotting import plot


class OrthogonalPolynomialsGenerator:
    """Orthogonal Polynomials Abstract Generator.

    Attributes:
        x (:obj: `sympy.Symbol`): variable of polynomials
        params (list): list of parameters
    """

    def __init__(self, x, params):
        self.x = x
        self.params = params
        self.generated = {}
        self.safe = {}
        self.clear()


    def __str__(self):
        raise NotImplementedError("Subclasses should implement this method")


    def clear(self):
        """Remove all polynomials previously calculated.
        """

        self.generated = {-1 : poly(0, self.x)}
        self.safe = {-1 : True}
    

    def _gen_explicit(self, n):
        """Generate the polynomial of degree n using the explicit formula
        """

        raise NotImplementedError("Subclasses should implement this method")


    def _recurrence_coeffs(self, n):
        """Calculate the coefficients of Three Term Recurrence formula
        """

        raise NotImplementedError("Subclasses should implement this method")


    def gen_poly(self, n):
        """Generate the polynomial of degree n.
        """
        if n < 0:
            n = -1
        if n not in self.generated:
            if n == -1:
                self.generated[n] = poly(0, self.x)
                self.safe = True
            elif n-1 in self.generated and n-2 in self.generated:
                coeffs = self._recurrence_coeffs(n)
                self.generated[n] = coeffs[0]*self.generated[n-1] + coeffs[1]*self.generated[n-2]
                self.safe[n] = False
            else:
                self.generated[n] = self._gen_explicit(n)
                self.safe[n] = True
        return self.generated[n]


    def sgen_poly(self, n):
        """Generate the polynomial of degree n safely.

        Note:
            This method uses only the explicit formula instead of recurrence formula and could be slower.
        """
        if n < 0:
            n = -1
        if n not in self.generated or (n in self.safe and not self.safe[n]):
            if n == -1:
                self.generated[n] = poly(0, self.x)
            else:
                self.generated[n] = self._gen_explicit(n)
            self.safe[n] = True
        return self.generated[n]


    def gen_ops(self, n):
        """Generate the Orthogonal Polynomials Sequence

        Args:
            n (int): maximum degree of generated polynomials
        """
        self.sgen_poly(-1)
        self.sgen_poly(0)
        for k in range(1, n):
            if not k in self.generated:
                coeffs = self._recurrence_coeffs(k)
                self.generated[k] = coeffs[0]*self.generated[k-1] + coeffs[1]*self.generated[k-2]
                self.safe[k] = False
        return [self.generated[i] for i in range(n)]


    def sgen_ops(self, n):
        """Generate the Orthogonal Polynomials Sequence safely

        Args:
            n (int): maximum degree of generated polynomials

        Note:
            This method uses only the explicit formula instead of recurrence formula and could be slower.
        """

        return [self.sgen_poly(k) for k in range(n)]


    def check(self, pol):
        """Check if a polynomial belongs to Charlier Orthogonal Sequence.

        Args:
            pol (sympy.poly): a polynomial

        Returns:
            The degree of pol and  its leading coefficient if pol belongs to sequence, -1 and 0 otherwise
        """

        n = degree(pol)
        if monic(self.gen_poly(n)).as_expr() == monic(pol).as_expr():
            return n, LC(pol)
        else:
            return -1, 0


    def plot(self, degrees):
        """Plot the Charlier polynomials of given degrees

        Args:
            degrees (list of int): degrees of plotted polynomials

        Return:
            Sympy plot
        """

        return plot(*[self.gen_poly(k).as_expr() for k in degrees], (self.x, 0, 10))