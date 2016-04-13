# -*- coding: UTF-8 -*-

import threading
from libnum.modular import invmod
from random import SystemRandom


c = []; d = []; R = []
L = 4
gen = SystemRandom()
match = False
points = {}
lock = threading.Lock()
coefficients = []
n = 0
matchPoint = 0

def generate_points(E, P, Q):
    global points, lock, match, coefficients, matchPoint, n
    an = gen.randrange(n)
    bn = gen.randrange(n)
    Xn = P*an + Q*bn
    while True:
        if Xn.y < 100:
            ct = threading.currentThread().getName()
            #print "{}: x = {}, y = {}\n".format(ct, Xn.x, Xn.y)
            pstr = "({}, {})".format(Xn.x, Xn.y)
            lock.acquire()
            if match == True:
                break

            if pstr in points.keys():
                match = True
                matchPoint = Xn
                #print "Thread {} found a match in point {}".format(ct, pstr)
                coefficients = [an, bn]
                break
            else:
                #print threading.currentThread().getName() + ' inserted {}-{}'.format(Xn, [an, bn])
                points[pstr] = [an, bn]
                lock.release()

        i = __H(Xn, L)
        Xn += R[i]
        an += c[i]
        bn += d[i]

    lock.release()

def parallelized(E, P, Q, numThreads):
    global n, matchPoint, points
    n = E.order()

    for i in range(L):
        c.append(gen.randrange(n))
        d.append(gen.randrange(n))
        R.append(P*c[-1] + Q*d[-1])

    for i in range(numThreads):
        trName = "tr{}".format(i)
        tr = threading.Thread(target=generate_points, args=(E, P, Q,), name=trName)
        tr.start()
        tr.join()

   # print points.items()
   # print "Match in {}".format(matchPoint)
    mstr = "({}, {})".format(matchPoint.x, matchPoint.y)
    if points.has_key(mstr):
        l = points.get(mstr)

    if (coefficients[1] == l[1]):
        raise ArithmeticError("Indefined value")

    f = l[0] - coefficients[0]
    g = invmod(coefficients[1]-l[1], n)
    ret = (f * g) % n
    return (ret + n) % n

def __H(P, L):
    return P.x % L
