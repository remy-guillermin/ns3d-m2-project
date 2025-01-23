#!/usr/bin/env python3
from fluiddyn.clusters.gricad import DahuGuix32_6130 as Cluster

cluster = Cluster(
    check_scheduler=False,
    options_guix_shell="-E ^OMPI -E ^OAR -E ^OMP -m manifest.scm -f python-fluidsim.scm",
)

cluster.commands_setting_env = [
    "source /applis/site/guix-start.sh",
    "source /etc/profile",
    "source ~/miniforge3/etc/profile.d/conda.sh",
    "conda activate env-fluidsim-mpi",
    "export OMPI_MCA_plm_rsh_agent=/usr/bin/oarsh",
    "export OMPI_MCA_btl_openib_allow_ib=true"
]

cluster.submit_command(
    command="--prefix $MPI_PREFIX \\\n  python simul_ns3d_forced_brunt.py --nx 256 --t_end 60",
    name_run="fluidsim-brunt",
    nb_nodes=2,
    nb_mpi_processes="auto",
    walltime="12:00:00",
    project="pr-strat-turb",
)