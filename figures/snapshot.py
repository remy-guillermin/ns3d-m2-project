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

Lx = sim.params.oper.Lx
Ly = sim.params.oper.Ly
Lz = sim.params.oper.Lz

with h5py.File(file_path, 'r') as hdf_file:
    u = hdf_file['state_phys/vx'][:]
    v = hdf_file['state_phys/vy'][:]
    w = hdf_file['state_phys/vz'][:]
    
# Compute the velocity magnitude
velocity_magnitude = np.sqrt(u**2 + v**2 + w**2)

# Grid dimensions
ez, ey, ex = velocity_magnitude.shape
x = np.linspace(0,Lx,ex)
y = np.linspace(0,Ly,ey)
z = np.linspace(0,Lz,ez)

# Plot the middle slice along the Z-axis
z_index = 0
plt.figure(figsize=(8, 6))
plt.contourf(x, y, velocity_magnitude[z_index, :, :], cmap='viridis')
plt.colorbar(label='Velocity magnitude ($m.s^{-1}$)')
plt.title(f'Velocity magnitude snapshot')
plt.xlabel('X')
plt.ylabel('Y')
plt.gca().set_aspect(1.0)
plt.show()