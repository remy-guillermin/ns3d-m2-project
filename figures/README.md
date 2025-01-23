# Figures
In this folder we regroup all the scripts/notebook used to plot figures/read data from the simulation file.


```
To display a video of this simulation, you can do:
fluidsim-ipy-load {sim.output.path_run}

sim.output.phys_fields.animate(dt_frame_in_sec=0.1, dt_equations=0.25, QUIVER=False, interactive=True, clim=(-1, 1))
sim.output.spectra.plot1d(tmin=period, plot_forcing_region=True, plot_dissipative_scales=True)
sim.output.spatial_means.plot()
sim.output.phys_fields.plot(time=period)
```