import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import glob
import ffmpeg
import progressBar
import h5py
from fluidsim import load_sim_for_plot

simul_name = 'ns3d_64x64x64_V3x3x3_2024-12-22_15-48-25/'
os.makedirs(f'iso_tests/{simul_name}', exist_ok=True)

print("Fetching simulation data")
sim_dir = '/Users/remyguillermin/Programmation/Etudes/M2/guillermin-m2/Sim_data/examples/test_iso3d/' + simul_name
sim = load_sim_for_plot(sim_dir, hide_stdout=True)
vx = sim.output.phys_fields.get_field_to_plot('vx', idx_time=0)[0]
vy = sim.output.phys_fields.get_field_to_plot('vy', idx_time=0)[0]
vz = sim.output.phys_fields.get_field_to_plot('vz', idx_time=0)[0]

print(
    f"""
To display a video of this simulation, you can do:
fluidsim-ipy-load {sim.output.path_run}

sim.output.phys_fields.animate(dt_frame_in_sec=0.1, dt_equations=0.1, QUIVER=False, interactive=True)

# you can start by plotting and explaining these figures
sim.output.spatial_means.plot()
sim.output.spatial_means.plot_dt_energy()
sim.output.spatial_means.plot_dt_enstrophy()

sim.output.spect_energy_budg.plot(tmin=4)

# write a script to plot the spectra...
sim.output.spectra.load1d_mean(tmin=4)

"""

)