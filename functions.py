import numpy as np

def lin(coefs, x):
    return coefs[0]*x+coefs[1]

def quadratic(coefs,x):
    return coefs[0]*x**2+coefs[1]*x+coefs[2]

def polinomial(coefs,x):
    r = 0
    for i in range(0, len(coefs)):
        r += coefs[i]*x**(len(coefs)-i)
    return r

def sin(x,A=1.,omega=1.,phi=0,c=0):
    return A*np.sin(omega*x+phi,c)

def cos(x,A=1.,omega=1.,phi=0,c=0):
    return A*np.cos(omega*x+phi,c)

def log(x,A=1,fac=0,c1=0,c2=0):
    return A*np.log(fac*x+c1)+c2

def exp(x,A=1,fac=1,c1=0,c2=0):
    return A*np.exp(fac*x+c1)+c2