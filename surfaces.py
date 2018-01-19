import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

r1 = np.arange(0, 1.01, 0.1)
r2 = np.arange(0, 1.01, 0.1)
r1, r2 = np.meshgrid(r1, r2)

z1 = -1*r1 - 1*r2 - 1
z2 = r2 - 1
z3 = -1*r2 - 1
z4 = r1 - 2

surf = ax.plot_surface(r1,r2,z1,color='blue',
                        linewidth=0, antialiased=False)
# ax.plot_wireframe(r1,r2,z1, color='blue', rstride=1, cstride=1)
ax.plot_wireframe(r1,r2,z2, color='red', rstride=5, cstride=5)
ax.plot_wireframe(r1,r2,z3, color='green', rstride=5, cstride=5)
ax.plot_wireframe(r1,r2,z4, color='yellow', rstride=5, cstride=5)

plt.show()


