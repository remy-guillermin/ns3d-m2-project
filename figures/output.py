import os
from fluidsim import load_sim_for_plot

file_name = 'ns3d_128x128x32_V3x3x0.75_2025-01-10_18-15-53.path'

with open(file_name, 'r') as file:
    simul_path = file.read().strip()

print("Fetching simulation data")
sim_dir = simul_path
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
"""
)
