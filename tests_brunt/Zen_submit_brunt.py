#!/usr/bin/env python3
from gricad_simple import Zen as Cluster

cluster = Cluster()

cluster.submit_command(
    command="python simul_ns3d_forced_brunt.py --nx 256 --t_end 60",
    name_run="fluidsim-test-brunt",
    nb_nodes=1,
    nb_cores_per_node=128,
    walltime="08:00:00",
)

