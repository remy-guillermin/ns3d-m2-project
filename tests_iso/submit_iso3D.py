#!/usr/bin/env python3
from gricad_simple import Zen as Cluster

cluster = Cluster()

cluster.submit_command(
    command="python simul_ns3d_forced_isotropic.py",
    name_run="fluidsim-test-iso",
    nb_nodes=1,
    nb_mpi_processes=8,
    walltime="00:30:00",
)

