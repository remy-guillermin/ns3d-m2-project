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

file_path = os.path.join(simul_path, 'spectra3d.h5')

period = 10 

with h5py.File(file_path, 'r') as hdf_file:
    k_spectra3d = dealias * hdf_file['k_spectra3d'][:]
    spectra_E = hdf_file['spectra_E'][:]
    times = hdf_file['times'][:]

filtered_spectra = spectra_E[times > period]

spectra_E_mean = np.mean(filtered_spectra, axis=0)

plt.figure(figsize=(7, 4))
plt.loglog(k_spectra3d, spectra_E_mean, 'k-')

plt.xlabel('k')
plt.ylabel('spectrum')

plt.title('3D spectrum')

plt.savefig('3d_spectrum.png', dpi=300)
print("Plot saved as '3d_spectrum.png'")
