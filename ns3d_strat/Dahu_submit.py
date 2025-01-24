#!/usr/bin/env python3
from fluiddyn.clusters.gricad import Dahu32_6130 as Cluster

cluster = Cluster()

cluster.commands_setting_env = [
        "source /etc/profile",
        f"source ~/miniforge3/etc/profile.d/conda.sh",
        "conda activate env-fluidsim-mpi",
    ]

cluster.submit_command(
    command="python simul_ns3d_strat_isotropic.py --nx 256 --t_end 60 --N 5.0",
    name_run="fluidsim-strat-256-5",
    nb_nodes=1,
    nb_mpi_processes="auto",
    walltime="23:59:00",
    project="pr-strat-turb",
)