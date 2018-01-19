import numpy as np
from scipy import optimize

minArr = np.zeros((4,2))

def fun0(x, arr):
    return x*arr[0,0] + (1-x)*arr[1,0] - x*arr[0,1] - \
            (1-x)*arr[1,1]

maxGap = 0
i = 0

for i in range(0,1):
# while i < 10000:

    # randTable = 10*np.random.rand(4,2) - 5
    randTable = np.array([[-2.495, -0.188],
            [4.622, -3.193],
            [-0.300, -0.659],
            [-1.250, 3.465]])

    sol0 = optimize.root(fun0, 0.5, args=randTable[0:2, 0:2],
            method='hybr') 
    sol1 = optimize.root(fun0, 0.5, args=randTable[2:4, 0:2],
            method='hybr') 

    p = sol0.x
    q = sol1.x
    r = np.sum(randTable[:,0]) / np.sum(randTable)

    if np.sum(np.array([p, q]) > 1) > 0:
        continue
    if np.sum(np.array([p, q]) < 0) > 0:
        continue

    i = i + 1

    print('\n#####################\nRound ', i, '\n\n')
    print('Table:\n', randTable)
    print('\np: ', p, '\tq: ', q, '\tr: ', r)

    val0 = np.dot(np.transpose([p,1-p,q,1-q]), randTable)
    miniMax = np.max(val0)
    val1 = np.dot(randTable, [r, 1-r])
    maxiMin = np.min(val1[0:2]) + np.min(val1[2:4])

    print('val0: ', val0, '\nval1:\n', val1)
    print('miniMax: ', miniMax, '\tmaxiMin: ', maxiMin)

    gap = (miniMax - maxiMin) / np.max(randTable)
    if gap > maxGap:
        maxGap = gap
        minArr = randTable

print(minArr, maxGap)
