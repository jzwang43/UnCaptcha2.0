import numpy as np

c = 0

f = open('data.csv', 'w+')
f.write('cv,nv,c')
for cv in np.linspace(.125, 2, 8):
    c += 1
    for nv in np.linspace(.125, cv + .125, c):
        f.write(str(cv) + ',' + str(nv) + ',' + str(c) + '\n')

f.close()
