import numpy as np


from devito import Grid, Eq, TimeFunction, Operator, Constant, solve
# Define some variables for problem setup
nx, ny, nz = 100, 100, 100
nu = .5
dx = 2./(nx - 1)
dy = 2./(ny - 1)
dz = 2./(nz - 1)
sigma = .25
dt = sigma * dx * dz * dy / nu
# Define staggered grid and field
grid = Grid(shape=(nx, ny, nz))
u = TimeFunction(name='u', grid=grid, space_order=2)
# Initialise field data
u.data[:, :, :] = 0.2
# Create an equation with second−order derivatives
a = Constant(name='a')
eq = Eq(u.dt, a*u.laplace, subdomain=grid.interior)
stencil = solve(eq, u.forward)
eq0 = Eq(u.forward, stencil)

op = Operator(eq0, opt=("advanced", {'linearize': True, 'omp-limit': 512}))
op.apply(time_M=10, dt=dt, a=nu)
print(np.linalg.norm(u.data))

u.data[:, :, :] = 0.2
op = Operator(eq0, opt=("advanced", {'linearize': False, 'omp-limit': 512}))
op.apply(time_M=10, dt=dt, a=nu)

print(np.linalg.norm(u.data))
op.apply(time_M=10, dt=dt, a=nu)
