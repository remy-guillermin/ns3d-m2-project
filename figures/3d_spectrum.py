from fluidsim import load_sim_for_plot
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import h5py

file_name = 'sim.path'

with open(file_name, 'r') as file:
    simul_path = file.read().strip()

simul_name = os.path.basename(simul_path.rstrip('/'))

sim = load_sim_for_plot(simul_path, hide_stdout=True)

dealias = sim.params.oper.coef_dealiasing

file_path = os.path.join(simul_path, 'spectra3d.h5')
period = 5

with h5py.File(file_path, 'r') as hdf_file:
    k_spectra3d = dealias * hdf_file['k_spectra3d'][:]
    spectra_E = hdf_file['spectra_E'][:]
    spectra_u = hdf_file['spectra_vx'][:]
    spectra_v = hdf_file['spectra_vy'][:]
    spectra_w = hdf_file['spectra_vz'][:]
    times = hdf_file['times'][:]

spectra_E_mean = np.mean(spectra_E, axis=1)
spectra_u_mean = np.mean(spectra_u, axis=1)
spectra_v_mean = np.mean(spectra_v, axis=1)
spectra_w_mean = np.mean(spectra_w, axis=1)

E_mean = np.mean(spectra_E_mean[times > period])
u_mean = np.mean(spectra_u_mean[times > period])
v_mean = np.mean(spectra_v_mean[times > period])
w_mean = np.mean(spectra_w_mean[times > period])

E_std = np.std(spectra_E_mean[times > period])
u_std = np.std(spectra_u_mean[times > period])
v_std = np.std(spectra_v_mean[times > period])
w_std = np.std(spectra_w_mean[times > period])

print(
    f'''
Mean energy : {E_mean:.5f} - Standard deviation : {E_std:.5f}
Mean energy along x : {u_mean:.5f} - Standard deviation : {u_std:.5f}
Mean energy along y : {v_mean:.5f} - Standard deviation : {v_std:.5f}
Mean energy along z : {w_mean:.5f} - Standard deviation : {w_std:.5f}
    '''
)

plt.figure(figsize=(5, 3))
plt.semilogy(times, spectra_E_mean, 'k--', label='$E_{tot}$')
plt.semilogy(times, spectra_u_mean, 'r-', label='$E_x$')
plt.semilogy(times, spectra_v_mean, 'g-', label='$E_y$')
plt.semilogy(times, spectra_w_mean, 'b-', label='$E_z$')

plt.axhline(E_mean, color='k', alpha=0.5, linestyle='--')
plt.axhline(u_mean, color='r', alpha=0.5, linestyle='--')
plt.axhline(v_mean, color='g', alpha=0.5, linestyle='--')
plt.axhline(w_mean, color='b', alpha=0.5, linestyle='--')

plt.xlabel('time ($s$)')
plt.ylabel('spectra')

plt.ylim(bottom=10**-6)

plt.legend()

plt.savefig('3d_spectra_time.png', dpi=300)
print("Plot saved as '3d_spectrum_time.png'")
