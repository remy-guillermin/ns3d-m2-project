import os
from math import pi
import argparse

from fluiddyn.util.mpi import printby0

from fluidsim.solvers.ns3d.strat.solver import Simul

parser = argparse.ArgumentParser()

parser.add_argument(
    "--nx",
    type=int,
    default=256,
    help="Number of grid points in the x direction.",
)
parser.add_argument(
    "--t_end", 
    type=float, 
    default=20.0, 
    help="End time of the simulation"
)
parser.add_argument(
    "--N",
    type=float,
    default=10.0,
    help="Brunt Vaisala frequency",
)

args = parser.parse_args()

if "FLUIDSIM_TESTS_EXAMPLES" in os.environ:
    t_end = 1.0
    nx = 24
else:
    t_end = args.t_end
    nx = args.nx

params = Simul.create_default_params()

params.output.sub_directory = "ns3d_strat"

ny = nx
nz = nx / 4
Lx = 3
params.oper.nx = nx
params.oper.ny = ny
params.oper.nz = nz
params.oper.Lx = Lx
params.oper.Ly = Ly = Lx / nx * ny
params.oper.Lz = Lz = Lx / nx * nz

delta_kx = 2 * pi / params.oper.Lx
delta_ky = 2 * pi / params.oper.Ly
delta_kz = 2 * pi / params.oper.Lz

params.time_stepping.USE_T_END = True
params.time_stepping.t_end = t_end

Lfh = 1.0
injection_rate = 1.0
Uh = (injection_rate * Lfh) ** (1 / 3)

# Brunt Vaisala frequency
params.N = args.N
if params.N != 0:
    Fh = Uh / (params.N * Lfh)
    period_N = 2 * pi / params.N
else:
    Fh = None
    period_N = 1.0
printby0(f"Input horizontal Froude number: {Fh:.3g}")

dx = Lx / nx
epsilon = 1.0
k_max = delta_kz * nz / 2
eta = 1.0 / k_max
nu = eta ** (4 / 3) * epsilon ** (1 / 3)
setattr(params, f"nu_2", nu)

printby0(f"nu_2 = {nu:.3e}")
printby0(f"eta = {eta:.4}")
printby0(f"k_max eta = {k_max*eta:.2e}")

params.init_fields.type = "noise"
params.init_fields.noise.length = 1.0
params.init_fields.noise.velo_max = 0.1

params.forcing.enable = True
params.forcing.type = "tcrandom"
params.forcing.normalized.constant_rate_of = None
params.forcing.nkmin_forcing = 3
params.forcing.nkmax_forcing = 4
# solenoidal field (toroidal + poloidal)
params.forcing.key_forced = ["vt_fft", "vp_fft"]
# forcing rate **per key forced**
params.forcing.forcing_rate = 0.5 * epsilon

params.output.periods_print.print_stdout = 1e-1

params.output.periods_save.phys_fields = 10.0
params.output.periods_save.spatial_means = 0.1
params.output.periods_save.spectra = 0.1
params.output.periods_save.spect_energy_budg = 0.1

params.output.periods_save.temporal_spectra = period_N / 4

params.output.spectra.kzkh_periodicity = 1

sim = Simul(params)
sim.time_stepping.start()