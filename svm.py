from sklearn.svm import SVC
import numpy as np
from numpy import *
from pylab import *
import sys

def train(X, Y, model, k='rbf', c=1.0, r=0.0, g=1.0, d=3, prob=False, quiet=True):
    if not quiet:
      print('training model %s -> %s\n' % (filename,model))
    if k not in ['linear','poly','rbf','tanh']:
      raise Exception('invalid argument: ' + k)
    c = float(c)
    r = float(r)
    g = float(g)
    d = float(d)

    f = SVC(C=c, kernel=k, degree=d, gamma=g, coef0=r,probability=prob)
    f.fit(X,Y)
    if not quiet:
      print('fit model:', f)#, file=sys.stderr)
    with open(model, 'w') as h:
        possv,negsv = 0,0
        for alpha in f.dual_coef_[0]:
            if alpha < 0: negsv += 1
            else: possv += 1
        print('svm_type c_svc', file=h)
        print('kernel_type', k, file=h)
        print('gamma', g, file=h)
        print('degree', d, file=h)
        print('coef0', r, file=h)
        print('nr_class', 2, file=h)
        print('total_sv', np.sum(f.n_support_), file=h)
        print('rho', -f.intercept_[0], file=h)
        print('label -1 1', file=h)
        print('nr_sv', possv, negsv, file=h)
        print('SV', file=h)
        for i,alpha in enumerate(f.dual_coef_[0]):
            if alpha < 0: continue
            print(str(alpha) + ' ' + ' '.join([str(fn+1)+':'+str(fv) for fn,fv in enumerate(f.support_vectors_[i])]), file=h)
        for i,alpha in enumerate(f.dual_coef_[0]):
            if alpha > 0: continue
            print(str(alpha) + ' ' + ' '.join([str(fn+1)+':'+str(fv) for fn,fv in enumerate(f.support_vectors_[i])]), file=h)
    return f

from numpy import *

def readData(filename):
    h = open(filename, 'r')
    Y = []
    X = []
    for l in h.readlines():
        a = l.strip().split()
        y = float(a[0])
        x1 = float(a[1])
        x2 = float(a[2])
        Y.append(y)
        X.append(array([x1,x2]))
    h.close()
    return (array(X),array(Y))

def plotData(X,Y):
    plot(X[Y>=0,0], X[Y>=0,1], 'bs', markersize=5)
    plot(X[Y< 0,0], X[Y< 0,1], 'ro', markersize=6)
    
def loadLibSVMModel(filename):
    h = open(filename, 'r')
    params = {}
    svs = []
    alpha = []
    inHeader = True
    for l in h.readlines():
        l = l.strip()
        if l == "SV":
            inHeader = False
        elif inHeader:
            a = l.split()
            params[a[0]] = a[1:]
        else:
            a = l.split()
            y = float(a[0])
            x1 = float(a[1][2:])
            x2 = float(a[2][2:])
            alpha.append(y)
            svs.append(array([x1,x2]))
    h.close()
    return (params, array(alpha), array(svs))

def plotSVS(alpha, svs):
    plot(svs[alpha>0,0], svs[alpha>0,1], 'bs', markersize=10)
    plot(svs[alpha<0,0], svs[alpha<0,1], 'ro', markersize=11)

def computeKernel(params, alpha, svs, D):
    if params['kernel_type'][0] == 'linear':
        rho    = float(params['rho'][0])
        return sum(alpha * dot(D, svs.T), axis=1) - rho
    if params['kernel_type'][0][:4] == 'poly':
        degree = float(params['degree'][0])
        gamma  = float(params['gamma'][0])
        coef0  = float(params['coef0'][0])
        rho    = float(params['rho'][0])
        # (gamma*u'*v + coef0)^degree
        return sum(alpha * ((gamma * dot(D, svs.T) + coef0) ** degree), axis=1) - rho
    if params['kernel_type'][0] == 'rbf':
        gamma  = float(params['gamma'][0])
        rho    = float(params['rho'][0])
        # exp(-gamma*|u-v|^2)
        N = D.shape[0]
        Z = zeros((N,)) - rho
        for i in range(alpha.shape[0]):
            v = repeat(reshape(svs[i,:],(1,2)),N,axis=0) - D
            Z = Z + alpha[i] * exp(-gamma*sum(v*v,axis=1))
        return Z
    if params['kernel_type'][0][:3] == 'sig':
        gamma  = float(params['gamma'][0])
        coef0  = float(params['coef0'][0])
        rho    = float(params['rho'][0])
        # tanh(gamma*u'*v + coef0)
        return sum(alpha * (tanh(gamma * dot(D, svs.T) + coef0)), axis=1) - rho
    raise Exception('unknown kernel type: ' + params['kernel_type'][0])
        
        
        
def plotContour(params, alpha, svs, resolution=0.005):
    n = len(arange(0,1,resolution))
    X0 = arange(0,1,resolution) * ones((n,n)) - 0.5
    Y0 = X0.T
    D = array([X0.reshape(-1), Y0.reshape(-1)]).T
    K = computeKernel(params, alpha, svs, D)
    Z = K.reshape((n,n))
    numCont = 100
    colors = []
    half = int(numCont/2)
    for i in range(numCont):
        r = 0
        b = 0
        if i < half:
            b = 0.25 + (half - i) / float(half) * 2/4
        else:
            r = 0.25 + (i - half) / float(half) * 2/4
        colors.append((r,0,b))
    Zmax = abs(Z).max()
    levels = arange(-Zmax,Zmax,Zmax/50)
    contourf(X0, Y0, -Z, levels=levels,colors=colors)
    contour(X0, Y0, Z, levels=[0], linewidths=[5], colors='w')
    contour(X0, Y0, Z, levels=[-1], linewidths=[2], colors='w', linestyles='dashed')
    contour(X0, Y0, Z, levels=[1], linewidths=[2], colors='w', linestyles='dashed')
    return Z
    
def plotAll(X, Y, params, alpha, svs):
    #figure(1)
    #hold(True)
    Z = plotContour(params, alpha, svs)
    plotData(X,Y)
    plotSVS(alpha, svs)
    #show()
    return Z

def drawBoundary(X,Y,modelName):
    (params,alpha,svs) = loadLibSVMModel(modelName)
    Z = plotAll(X,Y,params,alpha,svs)
