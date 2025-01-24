# Isotropic tests scripts
In this folder we regroup the content of the [folder of Wesley Agoua about isotropic tests](https://gricad-gitlab.univ-grenoble-alpes.fr/legi/post-doc/2024/2024-postdoc-agoua-wesley/-/tree/main/test_iso) with modifications so that it can be used during this project.

## Computing setup 
Don't forget to execute `source /applis/site/guix-start.sh` when logging in on Dahu!

### Dahu Cluster (With Guix)
We try to use the Guix configuration to submit our job but it doesn't work now.

Submit job with 
```sh
python Guix_Dahu_submit_iso3D.py
```

Not working as of today (Thursday 9<sup>th</sup> January), with the following error message

```text
----------------------------------------------------------------------------
prterun was unable to find the specified executable file, and therefore did
not launch the job.  This error was first reported for process rank
0; it may have occurred for other processes as well.

NOTE: A common cause for this error is misspelling a prterun command
   line parameter option (remember that prterun interprets the first
   unrecognized command line token as the executable).

Node:       dahu44 Executable: python
----------------------------------------------------------------------------
```

when running the following script [`Guix_submit.py`](./Guix_submit.py)
```python
#!/usr/bin/env python3
from gricad_simple import DahuGuix32_6130 as Cluster

cluster = Cluster()

cluster.submit_command(
    command="python simul_ns3d_forced_isotropic.py --nx 32 --t_end 20",
    name_run="fluidsim-test-iso",
    nb_nodes=2,
    nb_mpi_processes="auto",
    walltime="00:30:00",
    project="pr-strat-turb",
)
```

### Dahu Cluster (With Miniconda)
We can submit job on Dahu without using Guix by using a conda env and the script [`Dahu_submit.py`](./Dahu_submit.py). 

Submit job with
```sh
python Dahu_submit_iso3D.py
```

> **Warning**  
> It is important to note that we are not able to use more than one MPI process for the moment.
> 
> The problem is that when more than one mpi process is specified, *i.e.* when `nb_mpi_processes="auto"`, the command 
> ```python
> python simul_ns3d_forced_isotropic.py --nx 32 --t_end 20
> ``` 
> is run multiple times instead of one time using parallelization. 


> **Update$$
> Now the mpi parallelization works on Dahu with Miniconda, I just needed to update my miniforge3 configuration
> 


### Zen Cluster
Because I have access to Mesonet server for my academic year, I tried to submit job on this cluster also, which works well after writing [`Zen_submit.py`](./Zen_submit.py).

Submit job with
```sh
./Zen_submit_iso3D.py
```

On this cluster everything works just fine, i have been able to compute a 128x128x32 simulation of 60 seconds in less than 30 minutes. 


