# Brunt Väisälä forced tests
In this folder we regroup all the scripts used to compute basic simulation with an anisotropic forcing with a fixed Brunt Väisälä frequency.

We will use Zen to compute 128x128x32 simulation as it is the easiest to use as of the 10<sup>th</sup> January 2025. 

The simulation parameters are based on [turb_trandom_anisotropic.py](https://foss.heptapod.net/fluiddyn/fluidsim/-/blob/branch/default/fluidsim/util/scripts/turb_trandom_anisotropic.py) from `fluidsim/util/scripts`

You can submit job on Zen with
```sh
./Zen_submit_iso3D.py
```