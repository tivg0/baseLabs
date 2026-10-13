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

def sin(coefs, x):
    return coefs[0]*np.sin(coefs[1]*x+coefs[2])+coefs[3]

def cos(coefs, x):
    return coefs[0]*np.cos(coefs[1]*x+coefs[2])+coefs[3]

def log(coefs, x):
    return coefs[0]*np.log(coefs[1]*x+coefs[2])+coefs[3]

def exp(coefs, x):
    return coefs[0]*np.exp(coefs[1]*x)+coefs[2]

def inverse(coefs, x):
    return coefs[0]/x+coefs[1]

def inversesqrt(coefs, x):
    return coefs[0]/x**(1/10)+coefs[1]