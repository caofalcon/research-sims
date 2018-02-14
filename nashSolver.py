def systemOfEquations(V, f):
    """
    V[i,j] = V^{(i+1)}_{(j+1)} in the game
    """

    ep = '(%d*r1+%d*r2+%d*(1-r1-r2))-(%d*r1+%d*r2+%d*(1-r1-r2))*(%.15f*q+1-q);' % \
            (V[0,0],V[1,0],V[2,0],V[0,1],V[1,1],V[2,1],f)
    eq = '(%d*r1+%d*r2+%d*(1-r1-r2))-(%d*r1+%d*r2+%d*(1-r1-r2))*(p+%.15f*(1-p));' % \
            (V[0,2],V[1,2],V[2,2],V[0,1],V[1,1],V[2,1],f) 
    er1 = '(%d*p*q+(%d-%d)*p-%d*q+(%d+%d))-(%d*p*q+(%d-%d)*p-%d*q+(%d+%d));' % \
            (V[1,1],V[1,0],V[1,1],V[1,2],V[1,1],V[1,2],V[2,1],V[2,0],V[2,1],V[2,2],V[2,1],V[2,2])
    er2 = '(%d*p*q+(%d-%d)*p-%d*q+(%d+%d))-(%d*p*q+(%d-%d)*p-%d*q+(%d+%d));' % \
            (V[0,1],V[0,0],V[0,1],V[0,2],V[0,1],V[0,2],V[2,1],V[2,0],V[2,1],V[2,2],V[2,1],V[2,2])
    er3 = '(%d*p*q+(%d-%d)*p-%d*q+(%d+%d))-(%d*p*q+(%d-%d)*p-%d*q+(%d+%d));' % \
            (V[0,1],V[0,0],V[0,1],V[0,2],V[0,1],V[0,2],V[1,1],V[1,0],V[1,1],V[1,2],V[1,1],V[1,2])

    eqs0 = [ep,eq,er1,er2]
    eqs1 = [ep,eq,er1,'r1;']
    eqs2 = [ep,eq,er2,'r2;']
    eqs3 = [ep,eq,er3,'1-r1-r2;']

    return [eqs0,eqs1,eqs2,eqs3]

def solve4Nash(syst, debug=True):
    from phcpy.solver import solve
    from phcpy.solutions import strsol2dict, is_real
    result = []

    for eqIdx, eqs in enumerate(syst):
        sols = solve(eqs, verbose=False)
        if debug:
            print('system', eqIdx, 'has', len(sols), 'solutions')
        for sol in sols:
            if is_real(sol, 1.0e-8):
                soldic = strsol2dict(sol)
                solvars = [soldic['p'].real, soldic['q'].real, soldic['r1'].real, soldic['r2'].real]
                if debug:
                    print('[p, q, r1, r2]', solvars)
                if all((solvar>=-1.0e-8 and solvar<=1+1.0e-8) for solvar in solvars):
                    result.append(solvars)
                elif debug:
                    print('[p, q, r1, r2]', solvars, 'real but falls outside of bounds.')

    return result

def evaluateUtility(V, x):
    return x[2]*(V[0,1]*x[0]*x[1]+(V[0,0]-V[0,1])*x[0]-V[0,2]*x[1]+(V[0,1]+V[0,2])) + \
            x[3]*(V[1,1]*x[0]*x[1]+(V[1,0]-V[1,1])*x[0]-V[1,2]*x[1]+(V[1,1]+V[1,2])) + \
            (1-x[2]-x[3])*(V[2,1]*x[0]*x[1]+(V[2,0]-V[2,1])*x[0]-V[2,2]*x[1]+(V[2,1]+V[2,2]))

def main():
    import matplotlib.pyplot as plt
    import numpy as np
    import sys

    debug = False

    if len(sys.argv[1:]) != 9:
        V = np.array([[2,1,0],[0,2,1],[1,0,2]], dtype=np.int)
    else:
        V = np.array(sys.argv[1:])
        V = V.astype(np.float)
        V = np.reshape(V, (3,3))

    r0 = []
    r1 = []
    r2 = []
    r3 = []

    for f in np.arange(0,10,0.01):
        if debug:
            print('f', f)
        nashList = solve4Nash(systemOfEquations(V, f), debug)
        for mne in nashList:
            U = evaluateUtility(V,mne)

            if mne[2] <= 1.0e-8:
                if evaluateUtility(V,[mne[0], mne[1], 1, 0, 0]) > evaluateUtility(V,[mne[0], mne[1], 0, 1, 0]) or \
                        evaluateUtility(V,[mne[0], mne[1], 1, 0, 0]) > evaluateUtility(V,[mne[0], mne[1], 0, 0, 1]):
                    continue
                r1.append([f, U])
            elif mne[3] <= 1.0e-8:
                if evaluateUtility(V,[mne[0], mne[1], 0, 1, 0]) > evaluateUtility(V,[mne[0], mne[1], 1, 0, 0]) or \
                        evaluateUtility(V,[mne[0], mne[1], 0, 1, 0]) > evaluateUtility(V,[mne[0], mne[1], 0, 0, 1]):
                    continue
                r2.append([f, U])
            elif 1-mne[2]-mne[3] <= 1.0e-8:
                if evaluateUtility(V,[mne[0], mne[1], 0, 0, 1]) > evaluateUtility(V,[mne[0], mne[1], 1, 0, 0]) or \
                        evaluateUtility(V,[mne[0], mne[1], 0, 0, 1]) > evaluateUtility(V,[mne[0], mne[1], 0, 1, 0]):
                    continue
                r3.append([f, U])
            else:
                r0.append([f, U])

            if debug:
                print('[p, q, r1, r2]', mne)
                print('U', U)

    fig, ax = plt.subplots()
    
    ax.scatter([x[0] for x in r0], [x[1] for x in r0], c='k', label='r* > 0')
    ax.scatter([x[0] for x in r1], [x[1] for x in r1], c='r', marker='x', label='r1 = 0')
    ax.scatter([x[0] for x in r2], [x[1] for x in r2], c='g', marker='+', label='r2 = 0')
    ax.scatter([x[0] for x in r3], [x[1] for x in r3], c='b', marker='.', label='1 - r1 - r2 = 0')
    
    legend = ax.legend(loc='best', shadow=True)
    plt.title(str(V))
    plt.xlabel('f(2)')
    plt.show()

if __name__ == "__main__":
    main()
