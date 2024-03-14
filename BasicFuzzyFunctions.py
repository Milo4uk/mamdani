import numpy as np

def Trap(x,a,b,c,d):
    if a<=x<=b:
        return (x-a)/(b-a)
    elif b<=x<=c:
        return 1
    elif c<=x<=d:
        return (d-x)/(d-c)
    else:
        return 0
    
def S(x,a,b):
    if a<=x<=b:
        return (x-a)/(b-a)
    elif x>=b:
        return 1
    else:
        return 0 
    
def Z(x,a,b):
    if x<=a:
        return 1
    elif a<=x<=b:
        return (b-x)/(b-a)
    else:
        return 0
    
def SmTrap(x,a,b,c,d):
    if a<=x<=(a+b)/2:
        return 2*(((x-a)/(b-a))**2)
    elif (a+b)/2<=x<=b:
        return 1-2*(((b-x)/(b-a))**2)
    elif b<=x<=c:
        return 1
    elif c<=x<=(c+d)/2:
        return 1-2*(((x-c)/(d-c))**2)
    elif (c+d)/2<=x<=d:
        return 2*(((d-x)/(d-c))**2)
    else:
        return 0
        
  

def SmS(x,a,b):
    if a<=x<=(a+b)/2:
        return 2*(((x-a)/(b-a))**2)
    elif (a+b)/2<=x<=b:
        return 1-2*(((b-x)/(b-a))**2)
    elif x>=b:
        return 1
    else:
        return 0 
    
def SmZ(x,a,b):
    if x<=a:
        return 1
    elif a<=x<=(a+b)/2:
        return 1-2*(((x-a)/(b-a))**2)
    elif (a+b)/2<=x<=b:
        return 2*(((b-x)/(b-a))**2)
    else:
        return 0


def Centroid(X,Y):
    X=np.array(X)
    Y=np.array(Y)
    return np.sum(X*Y)/np.sum(Y)

def FirstMax(X,Y):
    X=np.array(X)
    Y=np.array(Y)
    mY=np.max(Y)
    A=[i for i in range(len(Y)) if Y[i]==mY]
    B=np.array([X[i] for i in A])
    return np.min(B)

def LastMax(X,Y):
    X=np.array(X)
    Y=np.array(Y)
    mY=np.max(Y)
    A=[i for i in range(len(Y)) if Y[i]==mY]
    B=np.array([X[i] for i in A])
    return np.max(B)

def AvgMax(X,Y):
    X=np.array(X)
    Y=np.array(Y)
    mY=np.max(Y)
    A=[i for i in range(len(Y)) if Y[i]==mY]
    B=np.array([X[i] for i in A])
    return np.mean(B)
