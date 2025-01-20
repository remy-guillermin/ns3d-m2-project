import argparse
import os

from fluiddyn.util.mpi import printby0
from math import pi, asin, sin

from fluidsim.solvers.ns3d.solver import Simul

parser = argparse.ArgumentParser()

parser.add_argument(
    "--nx",
    type=int,
    default=64,
    help="Number of grid points in the x direction.",
)
parser.add_argument(
    "--t_end", 
    type=float, 
    default=20.0,
    help="End time of the simulation"
)
parser.add_argument(
    "--order",
    type=int,
    default=2,
    help="Order of the viscosity (`2` corresponds to standard viscosity)",
)
parser.add_argument(
    "--N",
    type=float,
    default=10.0,
    help="Brunt-Väisälä frequency",
)
parser.add_argument(
        "--init-velo-max",
        type=float,
        default=0.01,
        help="params.init_fields.noise.max",
    )

max_elapsed = "23:50:00"

args = parser.parse_args()

t_end = args.t_end
nx = args.nx

params = Simul.create_default_params()

params.output.sub_directory = "test_Brunt3D"

ratio_nh_nz = 4

ny = nx
nz = nx / ratio_nh_nz
Lx = 1
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
params._set_attrib("N", None)
params.N = args.N
Fh = Uh / (args.N * Lfh)
print(f"Input horizontal Froude number: {Fh:.3g}")

Rb = 5.0
nu = injection_rate / (Rb * args.N**2)
params.nu_2 = nu

eta = (nu**3 / injection_rate) ** 0.25
k_max = delta_kz * nz / 2
print(f"{eta * k_max = :.3e}")

coef_nu4 = 1.0

if eta * k_max > 1:
    print("Well resolved simulation, no need for nu_4")
    params.nu_4 = 0.0
else:
    injection_rate_4 = injection_rate
    # only valid if R4 >> 1 (isotropic turbulence at small scales)
    params.nu_4 = (
        coef_nu4 * injection_rate_4 ** (1 / 3) / k_max ** (10 / 3)
    )
    Rb_4 = injection_rate / (params.nu_4 * args.N**4)
    print(
        f"Resolution too coarse, we add order-4 hyper viscosity nu_4={params.nu_4:.3e}."
    )

params.init_fields.type = "noise"
params.init_fields.noise.length = params.oper.Lz / 2
params.init_fields.noise.velo_max = args.init_velo_max

params.forcing.enable = True
params.forcing.type = "tcrandom_anisotropic"
params.forcing.forcing_rate = injection_rate
params.forcing.key_forced = ["vp_fft"]

def round3(number):
    return round(number, 3)

# Ratio omega_f / N, fixing the mean angle between the vertical and the forced wavenumber
F = 0.3
delta_F = 0.1

angle = asin(F)
delta_angle = asin(delta_F)

print(f"angle = {angle / pi * 180:.2f}°")
print(f"delta angle = {delta_angle / pi * 180:.2f}°")

kfh = 2 * pi / Lfh
kf = kfh / sin(angle)

ratio_kfmin_kf = 0.5
ratio_kfmax_kf = 2.0

kf_min = kf * ratio_kfmin_kf
kf_max = kf * ratio_kfmax_kf

params.forcing.nkmin_forcing = max(0, round3(kf_min / delta_kz))
params.forcing.nkmax_forcing = min(nz // 2, round3(kf_max / delta_kz))

period_N = 2 * pi / args.N
omega_l = args.N * F

# time_stepping fixed to follow waves
params.time_stepping.USE_T_END = True
params.time_stepping.t_end = args.t_end
params.time_stepping.max_elapsed = max_elapsed
params.time_stepping.deltat_max = min(0.1, period_N / 16)

# time_correlation is fixed to forced wave period
params.forcing.tcrandom.time_correlation = 2 * pi / omega_l
params.forcing.tcrandom_anisotropic.angle = round3(angle)
params.forcing.tcrandom_anisotropic.delta_angle = round3(delta_angle)
params.forcing.tcrandom_anisotropic.kz_negative_enable = True

params.output.periods_print.print_stdout = 1e-1

params.output.periods_save.phys_fields = 1.0
params.output.periods_save.spatial_means = 0.02
params.output.periods_save.spectra = 0.05
params.output.periods_save.spect_energy_budg = 0.1

params.output.spectra.kzkh_periodicity = 1

params.output.periods_save.spatiotemporal_spectra = period_N / 8

params.output.spatiotemporal_spectra.file_max_size = 80.0  # (Mo)
# probes_region in nondimensional units (mode indices).
ikzmax = 16
ikhmax = ikzmax * ratio_nh_nz
params.output.spatiotemporal_spectra.probes_region = (ikhmax, ikhmax, ikzmax)

sim = Simul(params)
sim.time_stepping.start()

file_name = os.path.basename(sim.output.path_run.rstrip('/')) + '.path'
with open(file_name, 'w') as file:
    file.write(sim.output.path_run)

print(
    f"""
Input horizontal Froude number: {Fh:.3g}

angle = {angle / pi * 180:.2f}°
delta angle = {delta_angle / pi * 180:.2f}°

To display a video of this simulation, you can do:
fluidsim-ipy-load {sim.output.path_run}

sim.output.phys_fields.animate(dt_frame_in_sec=1/30, dt_equations=0.15, QUIVER=False, interactive=True)

sim.output.spatial_means.plot_dt_E()
sim.output.spatial_means.plot()

sim.output.phys_fields.set_equation_crosssection("y=0")
sim.output.phys_fields.animate('vx', dt_frame_in_sec=0.3, dt_equations=0.25)

tmin = 15
sim.output.horiz_means.plot(tmax=tmin)
sim.output.horiz_means.plot(tmin=tmin)

sim.output.spectra.plot1d(coef_compensate=5/3, tmin=tmin)
sim.output.spect_energy_budg.plot_fluxes(tmin=tmin)

"""
)