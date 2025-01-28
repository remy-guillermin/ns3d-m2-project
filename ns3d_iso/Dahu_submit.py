#!/usr/bin/env python3
from fluiddyn.clusters.gricad import Dahu32_6130 as Cluster

cluster = Cluster()

cluster.commands_setting_env = [
        "source /etc/profile",
        f"source ~/miniforge3/etc/profile.d/conda.sh",
        "conda activate env-fluidsim-mpi",
    ]

cluster.submit_command(
    command="python simul_ns3d_forced_isotropic.py --nx 256 --t_end 60",
    name_run="fluidsim-iso-256",
    nb_nodes=1,
    nb_mpi_processes="auto",
    walltime="12:00:00",
    project="pr-strat-turb",
)