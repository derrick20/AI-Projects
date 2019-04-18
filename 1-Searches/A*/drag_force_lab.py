import numpy as np
from math import pi, atan, sin, cos
from matplotlib import pyplot as plt

c1, c2 = 1.12785751, 0.277220623

def projectile_with_drag(h, s, angle):
    g = 9.81
    v_x = s*cos(angle)
    v_y = s*sin(angle)
    v = (v_x, v_y) # initial velocity (x, y, |v|
    r = (0, h) # initial position
    d_t = 0.004166666 # 0.0041666...
    path_x = [r[0]] # x(t), y(t) tuples, so later we can graph it (t = index *  d_t)
    path_y = [r[1]]

    while r[1] > 0:
        v_mag = (v[0]**2 + v[1]**2)**0.5
        a_d = c1*v_mag + c2*(v_mag**2) # acceleration due to drag
        angle = atan(v[1]/v[0])
        a_x = -a_d * cos(angle)
        a_y = -a_d * sin(angle) - g
        #print((a_x, a_y))
        a = (a_x, a_y)
        dx = v[0]*d_t + 1/2 * a[0]*(d_t**2)
        dy = v[1]*d_t + 1/2 * a[1]*(d_t**2)
        r = (r[0] + dx, r[1] + dy) # incorporate change from acceleration/velocity
        path_x.append(r[0])
        path_y.append(r[1])

        v = (v[0] + a[0]*d_t, v[1] + a[1]*d_t) # the velocity changes after this moment due to acceleration by drag/gravity
    for i in path_x:
        print(i)
    for i in path_y:
        print(i)
    plt.plot(path_x, path_y)
    plt.title("Path of Projectile")
    plt.xlabel("Distance (m)")
    plt.ylabel("Height (m)")
    plt.show()

projectile_with_drag(0.492, 7.67, pi/4)

v = []
a = []

def calc_constants():
    with open("data.txt") as f:
        i = 0
        for line in f: # input data
            #print(line.rstrip().split(' '))
            vi, ai = [float(x) for x in line.rstrip().split()]
            v.append(vi)
            a.append(ai)
            i += 1
        # a12 = a21
        g = 9.81
        a11, a12, a22, b1, b2 = 0, 0, 0, 0, 0
        for i in range(len(v)):
            a11 += v[i]**2
            a12 += v[i]**3
            a22 += v[i]**4

            b1 += (g - a[i]) * v[i]
            b2 += (g - a[i]) * (v[i]**2)

        det = a11*a22 - a12**2

        A = np.matrix([[a11, a12], [a12, a22]])
        B = np.matrix([[b1], [b2]])
        print(A)
        print(B)
        print(A.I * B)
        #print ( (a11, a12, a22, b1, b2, det))

