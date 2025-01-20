#!/usr/bin/env python3
from gricad_simple import Dahu32_6130 as Cluster

cluster = Cluster()

cluster.submit_command(
    command="python simul_ns3d_forced_brunt.py --nx 256 --t_end 60",
    name_run="fluidsim-test-brunt",
    nb_nodes=1,
    nb_mpi_processes=1,
    walltime="01:00:00",
    project="pr-strat-turb",
)

