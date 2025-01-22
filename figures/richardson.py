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

N = sim.params.N
Lz = sim.params.oper.Lz
nz = sim.params.oper.nz
dz = Lz / nz

all_Ri = []

state_phys_pattern = 'state_phys*.h5'
state_phys_list = sorted(glob.glob(os.path.join(simul_path, state_phys_pattern))) 

for idx, file_path in enumerate(state_phys_list):
    with h5py.File(file_path, 'r') as f:
        u = f['state_phys/vx'][:]
        v = f['state_phys/vy'][:]
        
        uh = np.sqrt(u**2 + v**2)
        duh_dz = np.gradient(uh, dz, axis=0)
        Ri = (N**2 / (duh_dz**2)).ravel()
        
        all_Ri.append(Ri[Ri < 10])

all_Ri_array = np.concatenate(all_Ri)

np.save('richardson.npy', all_Ri_array)

print(f"Richardson numbers saved to 'richardson.npy'. Total size: {all_Ri_array.size}")

plt.figure(figsize=(8, 6))
plt.hist(all_Ri_array, bins=50, density=True, alpha=0.3, color='blue', edgecolor='black', label='Histogram')

# Compute and plot the KDE
kde = gaussian_kde(all_Ri_array)
x_vals = np.linspace(np.min(all_Ri_array), np.max(all_Ri_array), 500)
plt.plot(x_vals, kde(x_vals), color='red', linewidth=2, label='KDE')

plt.xlabel('Richardson Number (Ri)', fontsize=14)
plt.ylabel('Probability Density', fontsize=14)
plt.title('Histogram and KDE of Richardson Number', fontsize=16)
plt.legend(fontsize=12)
plt.grid(alpha=0.3)
plt.savefig('richardson_pdf.png', dpi=300)
print("Plot saved as 'richardson_pdf.png'")