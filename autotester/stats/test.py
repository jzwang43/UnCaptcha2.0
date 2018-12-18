import numpy as np

c = 0

f = open('data.csv', 'w+')
f.write('cv,nv,c')
i = 0
for cv in np.linspace(.125, 2, 8):
    c += 1
    for nv in np.linspace(.125, cv + .125, c):
        i += 1
        print(i)

f.close()
