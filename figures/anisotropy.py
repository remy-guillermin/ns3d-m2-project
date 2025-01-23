from fluidsim import load_sim_for_plot
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
import pandas as pd
import numpy as np
import os
import h5py

file_name = 'sim.path'

with open(file_name, 'r') as file:
    simul_path = file.read().strip()

simul_name = os.path.basename(simul_path.rstrip('/'))

sim = load_sim_for_plot(simul_path, hide_stdout=True)

init_file_path = os.path.join(simul_path, 'state_phys_t0001.001.h5')
end_file_path = os.path.join(simul_path, 'state_phys_t0027.001.h5')

Lx = sim.params.oper.Lx
Ly = sim.params.oper.Ly
Lz = sim.params.oper.Lz

with h5py.File(init_file_path, 'r') as hdf_file:
    ui = hdf_file['state_phys/vx'][:]
    vi = hdf_file['state_phys/vy'][:]
    wi = hdf_file['state_phys/vz'][:]
    
with h5py.File(end_file_path, 'r') as hdf_file:
    uf = hdf_file['state_phys/vx'][:]
    vf = hdf_file['state_phys/vy'][:]
    wf = hdf_file['state_phys/vz'][:]
    
# Compute the velocity magnitude
magnitude_i = np.sqrt(vi**2 + vi**2 + wi**2)
magnitude_f = np.sqrt(vf**2 + vf**2 + wf**2)


theta_i = np.arccos(wi/magnitude_i)
theta_f = np.arccos(wf/magnitude_f)

magnitude_i = magnitude_i.ravel()
magnitude_f = magnitude_f.ravel()

theta_i = theta_i.ravel()
theta_f = theta_f.ravel()


fig, axes = plt.subplots(1, 2, figsize=(16, 6))
axes[0].hist(magnitude_i, bins=50, density=True , alpha=0.3, color='blue', edgecolor='black', label='Histogram')

# Compute and plot the KDE
kde = gaussian_kde(magnitude_i)
x_vals = np.linspace(np.min(magnitude_i), np.max(magnitude_i), 500)  # Range for KDE
axes[0].plot(x_vals, kde(x_vals), color='red', linewidth=2, label='KDE')

# Add labels, title, and legend
axes[0].set_xlabel('Velocity magnitude ($m.s^{-1}$)', fontsize=14)
axes[0].set_ylabel('Probability Density', fontsize=14)
axes[0].set_title('$t=0$ s', fontsize=16)
axes[0].legend(fontsize=12)
axes[0].grid(alpha=0.3)

axes[1].hist(magnitude_f, bins=50, density=True , alpha=0.3, color='blue', edgecolor='black', label='Histogram')

kde = gaussian_kde(magnitude_f)
x_vals = np.linspace(np.min(magnitude_f), np.max(magnitude_f), 500) 
axes[1].plot(x_vals, kde(x_vals), color='red', linewidth=2, label='KDE')


axes[1].set_xlabel('Velocity magnitude ($m.s^{-1}$)', fontsize=14)
axes[1].set_ylabel('Probability Density', fontsize=14)
axes[1].set_title('$t=27$ s', fontsize=16)
axes[1].legend(fontsize=12)
axes[1].grid(alpha=0.3)
fig.suptitle("Histogram and KDE of velocity magnitude")

plt.savefig('magnitude_pdf.png', dpi=300)
print("Plot saved as 'magnitude_pdf.png'")

fig, axes = plt.subplots(1, 2, figsize=(16, 6))
axes[0].hist(theta_i, bins=50, density=True , alpha=0.3, color='blue', edgecolor='black', label='Histogram')

kde = gaussian_kde(theta_i)
x_vals = np.linspace(np.min(theta_i), np.max(theta_i), 500) 
axes[0].plot(x_vals, kde(x_vals), color='red', linewidth=2, label='KDE')

axes[0].set_xlabel('Velocity magnitude ($m.s^{-1}$)', fontsize=14)
axes[0].set_ylabel('Probability Density', fontsize=14)
axes[0].set_title('$t=0$ s', fontsize=16)
axes[0].legend(fontsize=12)
axes[0].grid(alpha=0.3)

axes[1].hist(theta_f, bins=50, density=True , alpha=0.3, color='blue', edgecolor='black', label='Histogram')

kde = gaussian_kde(theta_f)
x_vals = np.linspace(np.min(theta_f), np.max(theta_f), 500) 
axes[1].plot(x_vals, kde(x_vals), color='red', linewidth=2, label='KDE')

axes[1].set_xlabel('Velocity vertical angle ($rad$)', fontsize=14)
axes[1].set_ylabel('Probability Density', fontsize=14)
axes[1].set_title('$t=27$ s', fontsize=16)
axes[1].legend(fontsize=12)
axes[1].grid(alpha=0.3)
fig.suptitle("Histogram and KDE of velocity angle")

plt.savefig('angle_pdf.png', dpi=300)
print("Plot saved as 'angle_pdf.png'")