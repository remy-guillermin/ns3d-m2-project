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