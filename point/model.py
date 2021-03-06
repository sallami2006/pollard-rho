# -*- coding: UTF-8 -*-

from fractions import gcd
from libnum.modular import invmod

class Point(object):
    def __init__(self, curve=None, x=None, y=None):
        if curve is not None:
            self.curve = curve
            self.x = x
            self.y = y
        self.is_infinity = False

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return self.x != other.x or self.y != other.y

    def __add__(self, other):
        if (other.is_infinity):
            return other + self

        if (self != other and self.x == other.x):
            return PointAtInfinity()

        delta = (self == other and _lambda(self)) or _lambda(self, other)

        kx = (delta ** 2 - self.x - other.x) % self.curve.field
        ky = (delta * (self.x - kx) - self.y) % self.curve.field

        R = Point()
        R.curve = self.curve
        R.x = (kx < 0 and kx + self.curve.field) or kx
        R.y = (ky < 0 and ky + self.curve.field) or ky
        return R

    def __iadd__(self, other):
        return self + other

    def __sub__(self, other):
        return Point(self.curve, self.x, -self.y)

    def __mul__(self, n):
        Q = self; R = None

        if (n & 1):
            R = self

        n >>= 1
        while (n):
            Q += Q
            if (n & 1):
                R = (type(R) is Point and R + Q) or Q
            n >>= 1
        return R

    def __repr__(self):
        return '({self.x}, {self.y})'.format(self=self)

def _lambda(P, other=None):
    if other:
        Q = other
        a = (Q.y - P.y) % P.curve.field
        b = Q.x - P.x

        aux = abs(a)
        d = gcd(aux, b)

        a /= d; b /= d
        a = (a + P.curve.field) % P.curve.field
        if (a % b != 0):
            b = invmod(b, P.curve.field)
            return a * b % P.curve.field

        return a / b
    else:
        a = (3*P.x*P.x + P.curve.A) % P.curve.field
        b = 2*P.y

        aux = abs(a)
        d = gcd(aux, b)

        a /= d; b /= d
        a = (a + P.curve.field) % P.curve.field
        if (a % b != 0):
            b = invmod(b, P.curve.field)
            return a * b % P.curve.field

        return a / b

class PointAtInfinity(Point):
    def __init__(self):
        super(Point, self).__init__()
        self.is_infinity = True

    def __eq__(self, other):
        return other.is_infinity

    def __ne__(self, other):
        return not other.is_infinity

    def __add__(self, other):
        return other

    def __mul__(self, n):
        return PointAtInfinity()

    def __repr__(self):
        return 'Infinite'
