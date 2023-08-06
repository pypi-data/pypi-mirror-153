import numpy as np
def DRegionModel(z, it, f, vKp, f5SW, f6WA, dtype = np.float32):

    A0=np.array([1.0, 1.2, 1.4, 1.5, 1.6, 1.7, 3.0], dtype = dtype)
    A1=np.array([0.6, 0.8, 1.1, 1.2, 1.3, 1.4, 1.0], dtype = dtype)
    A2=np.array([0., 0., 0.08, 0.12, 0.05, 0.2, 0.], dtype = dtype)
    A3=np.array([0., 0., 0., 0., 0., 0., 1.0], dtype = dtype)
    A4=np.array([0., 0., -0.30, 0.10, 0.20, 0.30, 0.15], dtype = dtype)
    A5=np.array([0., -0.10, -0.20, -0.25, -0.30, -0.30, 0.], dtype = dtype)
    A6=np.array([0., 0.1, 0.3, 0.6, 1., 1., 0.7], dtype = dtype)
    pi=3.14159265
    #pi = dtype(np.pi)

    elg=np.array([0., 0., 0., 0., 0., 0., 0.])
    if z <= 45:
        f1z = dtype(1.)
    else:
        if (z < 90):
            f1z = dtype(1.1892*( np.cos(z*pi/180)))
            f1z = dtype(np.power(f1z,0.5))

        else:
            f1z = dtype(0.)
    #print (f1z)
    f4S = dtype(1.)
    if ((it >= 5) and (it  <= 9)):
        f4S = dtype(0.)
        f5SW = dtype(0.)
        f6WA = dtype(0.)

    if ((it == 3) or (it == 4) or (it == 10) or (it == 11)):
        f4S = dtype(0.5)
        f5SW = dtype(0.)
        f6WA = dtype(0.)

    f2Kp = dtype(vKp)
    if (vKp > 2):
        f2Kp=dtype(2.)
    f3F=dtype((f-60.)/300.*f1z)
    #print(f3F)
    for i in range(7):
        elg[i]=dtype(A0[i]+A1[i]*f1z+A2[i]*f2Kp+A3[i]*f3F+A4[i]*f4S+A5[i]*f5SW+A6[i]*f6WA)

    return elg