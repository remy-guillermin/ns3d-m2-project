#!/usr/bin/env python3
from gricad_simple import Zen as Cluster

cluster = Cluster()

cluster.submit_command(
    command="fluidfft-bench 1024 -d 3",
    name_run="bench_fluidfft",
    nb_nodes=1,
    nb_mpi_processes="auto",
    walltime="01:00:00",
)

