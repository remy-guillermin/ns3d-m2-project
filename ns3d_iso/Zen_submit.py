#!/usr/bin/env python3
from gricad_simple import Zen as Cluster

cluster = Cluster()

cluster.submit_command(
    command="python simul_ns3d_forced_isotropic.py --nx 256 --t_end 60",
    name_run="fluidsim-test-iso",
    nb_nodes=1,
    nb_cores_per_node=1,
    walltime="12:00:00",
)