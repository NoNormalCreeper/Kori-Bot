import math as m
# import random
from random import randint


def abs(x):
    return x if x>=0 else (-x)

def a0(x, a, b):
    return a*(x**2) + b*x

def b0(x, a, b):
    return a * m.sqrt(abs(b)*x)

def c0(x,a,b):
    return a*m.sin(b*x)

def d0(x,a,b):
    return a*m.cos(b*x)

def e0(x,a,b):
    return a**(b*x)

def f0(x,a,b):
    return a*m.log(abs(b),abs(x))

def g0(x,a,b):
    return a/x + b

def h0(x,a,b):
    return a*x+b

def i0(x,a,b):
    return a*m.factorial(x) + b

def j0(x,a,b):
    return (x**a)-(x**b)

def k0(x,a,b):
    return m.sin(a*x) * m.cos(x) * m.tan(x)

def l0(x,a,b):
    return a * m.sqrt(abs(b*m.log(abs(x))))

def m0(x,a,b):
    return a / (m.cos(b*x))

def n0(x,a,b):
    return m.exp(a*x)-m.log(abs(b*x))

def o0(x,a,b):
    return a*m.log(abs(m.sin(abs(b*x))))

def p0(x,a,b):
    return a*x + b/x

functions = [
    [a0, "{0}x^2+{1}x"],
    [b0, "{0}sqrt(|{1}|x)"],
    [c0, "{0}sin({1}x)"],
    [d0, "{0}cos({1}x)"],
    [e0, "{0}^({1}x)"],
    [f0, "{0}log(|{1}|,|x|)"],
    [g0, "({0}/x)+{1}"],
    [h0, "{0}x+{1}"],
    [i0, "{0}x!+{1}"],
    [j0, "x^{0} - x^{1}"],
    [k0, "sin({0}x)cos({1}x)tan(x)"],
    [l0, "{0}sqrt(|{1}ln(|x|)|)"],
    [m0, "{0}/(cos({1}x))"],
    [n0, "e^({0}x)-ln(|{1}x|)"],
    [o0, "{0}ln(|sin({1}x)|)"],
    [p0, "{0}x + {1}/x"],
]

range_1 = -3
range_2 = 5


def f(x: int):
    a = randint(range_1*10, range_2*10) / 10
    b = randint(range_1*10, range_2*10) / 10
    while a==1 or b==1:
        a = randint(range_1*10, range_2*10) / 10
        b = randint(range_1*10, range_2*10) / 10
    length = len(functions)
    no = randint(0, length-1)

    # x *= b
    try:
        y_0 = functions[no][0](x, a, b)
        y_1 = round(1000*y_0)/1000
        y = round(y_1)
        # func *= y
        if y > 777:
            y_2 = 777
        elif y < -777:
            y_2 = -777
        else:
            y_2 = y

        return [y_2, "x={0}, f(x)= {1} = {2} .".format(x, (functions[no][1].format(a,b)), y_1)]
    except:
        return [0, "Math error!"]