# Stratified run 

In this folder we will regroup the script used for running stratified simulations. The script [`simul_ns3d_strat_isotropic.py`](./simul_ns3d_strat_isotropic.py) is from the script [simul_ns3dstrat_forcing_random.py](https://foss.heptapod.net/fluiddyn/fluidsim/-/blob/branch/default/doc/examples/simul_ns3dstrat_forcing_random.py) from Fluidsim.

## Computing setup 
Don't forget to execute `source /applis/site/guix-start.sh` when logging in on Dahu!

### Dahu Cluster (With Miniconda)
We can submit job on Dahu without using Guix by using a conda env and the script [`Dahu_submit_iso3D.py`](./Dahu_submit_iso3D.py). 

Submit job with
```sh
python Dahu_submit.py
```
