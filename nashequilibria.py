import numpy as np
import sys
from scipy import optimize
import matplotlib.pyplot as plt

f = 1
X = np.zeros((3,12), dtype=float)


def fun(s):
    return [s[0] + s[1] - 1, s[2] + s[3] - 1, s[4] + s[5] + s[6] - 1,
            (X[0,0] - X[0,6])*s[2]*s[4] + (X[0,3] - X[0,9])*s[3]*s[4] + 
            (X[0,1] - X[0,7])*s[2]*s[5] + (X[0,4] - X[0,10])*s[3]*s[5] + 
            (X[0,2] - X[0,8])*s[2]*s[6] + (X[0,5] - X[0,11])*s[3]*s[6],
            (X[1,0] - X[1,3])*s[0]*s[4] + (X[1,6] - X[1,9])*s[1]*s[4] + 
            (X[1,1] - X[1,4])*s[0]*s[5] + (X[1,7] - X[1,10])*s[1]*s[5] + 
            (X[1,2] - X[1,5])*s[0]*s[6] + (X[1,8] - X[1,11])*s[1]*s[6],
            (X[2,0] - X[2,1])*s[0]*s[2] + (X[2,6] - X[2,7])*s[1]*s[2] + 
            (X[2,3] - X[2,4])*s[0]*s[3] + (X[2,9] - X[2,10])*s[1]*s[3],
            (X[2,1] - X[2,2])*s[0]*s[2] + (X[2,7] - X[2,8])*s[1]*s[2] +
            (X[2,4] - X[2,5])*s[0]*s[3] + (X[2,10] - X[2,11])*s[1]*s[3],
            ]

def util(s):
    return [
            [(X[0,0])*s[2]*s[4] + (X[0,3])*s[3]*s[4] + (X[0,1])*s[2]*s[5] + 
                (X[0,4])*s[3]*s[5] + (X[0,2])*s[2]*s[6] + (X[0,5])*s[3]*s[6],
                (X[1,0])*s[0]*s[4] + (X[1,6])*s[1]*s[4] + (X[1,1])*s[0]*s[5] + 
                (X[1,7])*s[1]*s[5] + (X[1,2])*s[0]*s[6] + (X[1,8])*s[1]*s[6],
                (X[2,0])*s[0]*s[2] + (X[2,6])*s[1]*s[2] + 
                (X[2,3])*s[0]*s[3] + (X[2,9])*s[1]*s[3],
                (X[2,1])*s[0]*s[2] + (X[2,7])*s[1]*s[2] +
                (X[2,4])*s[0]*s[3] + (X[2,10])*s[1]*s[3]
                ],
            [(X[0,6])*s[2]*s[4] + (X[0,9])*s[3]*s[4] + (X[0,7])*s[2]*s[5] + 
                (X[0,10])*s[3]*s[5] + (X[0,8])*s[2]*s[6] + (X[0,11])*s[3]*s[6],
                (X[1,3])*s[0]*s[4] + (X[1,9])*s[1]*s[4] + (X[1,4])*s[0]*s[5] + 
                (X[1,10])*s[1]*s[5] + (X[1,5])*s[0]*s[6] + (X[1,11])*s[1]*s[6],
                (X[2,1])*s[0]*s[2] + (X[2,7])*s[1]*s[2] + 
                (X[2,4])*s[0]*s[3] + (X[2,10])*s[1]*s[3],
                (X[2,2])*s[0]*s[2] + (X[2,8])*s[1]*s[2] +
                (X[2,5])*s[0]*s[3] + (X[2,11])*s[1]*s[3]
                ]
            ]

x = np.arange(0,10,0.01)
U = np.zeros((3,x.size))

if len(sys.argv[1:]) != 9:
    print("ERROR: incorrect system input, using default.")
    R = np.array([[3,0,0],[0,3,0],[0,0,3]])
else:
    R = np.array(sys.argv[1:])
    R = R.astype(np.float)
    R = np.reshape(R, (3,3))

print(R)

for idx, f in enumerate(x):
    # print('\nf(2) = ', f)
    X = np.array([ \
            [ R[0,0], R[1,0], R[2,0], R[0,0], R[1,0], R[2,0], f*R[0,1], f*R[1,1], f*R[2,1], R[0,1], R[1,1], R[2,1]],
            [ R[0,1], R[1,1], R[2,1], R[0,2], R[1,2], R[2,2], f*R[0,1], f*R[1,1], f*R[2,1], R[0,2], R[1,2], R[2,2]],
            [ -R[0,0]-R[0,1], -R[1,0]-R[1,1], -R[2,0]-R[2,1], -R[0,0]-R[0,2], -R[1,0]-R[1,2], -R[2,0]-R[2,2], 
                -R[0,1], -R[1,1], -R[2,1], -R[0,1]-R[0,2], -R[1,1]-R[1,2], -R[2,1]-R[2,2]]
            ])
    sol = optimize.root(fun, [0.618,0.382,0.618,0.382,0.3,0.4,0.3])
    # print('Solution: ', sol.x)
    if np.sum(np.array(sol.x) < 0) > 0:
        print('Error: solution has negative probability at f(2) = ', f)
        print(sol.x)
        break
    util_sol_x_ = util(sol.x)
    # print(util_sol_x_)
    U[:,idx] = util_sol_x_[0][0:3]
    
fig, ax = plt.subplots()
ax.plot(x, U[0], 'r--', label='U_1')
ax.plot(x, U[1], 'b:', label='U_2')
ax.plot(x, U[2], 'k', label='U_3')

legend = ax.legend(loc='best', shadow=True)

plt.title(str(sys.argv[1:]))
plt.xlabel('f(2)')
plt.show()

