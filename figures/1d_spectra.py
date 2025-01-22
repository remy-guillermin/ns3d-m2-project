from fluidsim import load_sim_for_plot
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
import pandas as pd
import numpy as np
import os
import glob
import h5py

file_name = 'sim.path'

with open(file_name, 'r') as file:
    simul_path = file.read().strip()

simul_name = os.path.basename(simul_path.rstrip('/'))

sim = load_sim_for_plot(simul_path, hide_stdout=True)

dealias = sim.params.oper.coef_dealiasing
eta = sim.output.spatial_means.get_dimless_numbers_averaged()['dimensional']['eta']
kmin_forcing = sim.params.forcing.nkmin_forcing
kmax_forcing = sim.params.forcing.nkmax_forcing

file_path = os.path.join(simul_path, 'spectra1d.h5')

diss_length = dealias * np.pi / (2 * eta)

period = 10

with h5py.File(file_path, 'r') as hdf_file:
    kx = dealias * hdf_file['kx'][:]
    ky = dealias * hdf_file['ky'][:]
    kz = dealias * hdf_file['kz'][:]
    spectra_E_kx = hdf_file['spectra_E_kx'][:]
    spectra_E_ky = hdf_file['spectra_E_ky'][:]
    spectra_E_kz = hdf_file['spectra_E_kz'][:]
    times = hdf_file['times'][:]
    
filtered_spectra_E_kx = spectra_E_kx[times > period]
filtered_spectra_E_ky = spectra_E_ky[times > period]
filtered_spectra_E_kz = spectra_E_kz[times > period]

spectra_E_kx_mean = np.mean(filtered_spectra_E_kx, axis=0)
spectra_E_ky_mean = np.mean(filtered_spectra_E_ky, axis=0)
spectra_E_kz_mean = np.mean(filtered_spectra_E_kz, axis=0)

plt.figure(figsize=(7, 4))

plt.loglog(kx, spectra_E_kx_mean, 'r-', label='$E(k_x)$')
plt.loglog(ky, spectra_E_ky_mean, 'g-', label='$E(k_y)$')
plt.loglog(kz, spectra_E_kz_mean, 'b-', label='$E(k_z)$')

plt.axvline(x = diss_length, color = 'k')

plt.xlabel('$k_x, k_y, k_z$')
plt.ylabel('spectra')

plt.legend()
plt.title('1D Spectra')
plt.savefig('1d_spectra.png', dpi=300)
print("Plot saved as '1d_spectra.png'")
