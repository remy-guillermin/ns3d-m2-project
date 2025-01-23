import os

from fluiddyn.util.mpi import printby0

from fluidsim.solvers.ns3d.strat.solver import Simul

if "FLUIDSIM_TESTS_EXAMPLES" in os.environ:
    t_end = 1.0
    nx = 24
else:
    t_end = 30.0
    nx = 256

params = Simul.create_default_params()

params.output.sub_directory = "examples"

ny = nx
nz = nx / 4
Lx = 3
params.oper.nx = nx
params.oper.ny = ny
params.oper.nz = nz
params.oper.Lx = Lx
params.oper.Ly = Ly = Lx / nx * ny
params.oper.Lz = Lz = Lx / nx * nz

params.time_stepping.USE_T_END = True
params.time_stepping.t_end = t_end

Lfh = 1.0
injection_rate = 1.0
Uh = (injection_rate * Lfh) ** (1 / 3)

# Brunt Vaisala frequency
params._set_attrib("N", None)
params.N = 10.0
Fh = Uh / (10.0 * Lfh)
print(f"Input horizontal Froude number: {Fh:.3g}")

n = 8
C = 1.0
dx = Lx / nx
B = 1
D = 1
eps = 1e-2 * B ** (3 / 2) * D ** (1 / 2)
params.nu_8 = (dx / C) ** ((3 * n - 2) / 3) * eps ** (1 / 3)

printby0(f"nu_8 = {params.nu_8:.3e}")

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
params.forcing.forcing_rate = 0.5 * eps

params.output.periods_print.print_stdout = 1e-1

params.output.periods_save.phys_fields = 0.5
params.output.periods_save.spatial_means = 0.1
params.output.periods_save.spectra = 0.1
params.output.periods_save.spect_energy_budg = 0.1

params.output.spectra.kzkh_periodicity = 1

sim = Simul(params)
sim.time_stepping.start()
