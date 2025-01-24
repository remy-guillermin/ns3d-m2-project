# Project Graduate School Remy Guillermin

## Setup

You can build this project using the Makefile :
- `make` builds [draft.pdf](draft/draft.tex), [report.pdf](report/report.tex) and [slide.pdf](slides/slide.tex).
- `make filename.pdf` builds either of the two pdf.
- `make env-fluidsim-mpi` builds the conda environment used in this project using [environment.yml](environment.yml).
  

## Cleaning

You can clean various parts of the project using the Makefile :
- `make cleanaux` will remove all the files created when building the pdf files.
- `make cleanpdf` will remove all the pdf builded.
- `make cleanenv` will remove the conda environment.
- `make clean` will execute all the previous command at once.

## Links

- This repository: https://gricad-gitlab.univ-grenoble-alpes.fr/legi/stage/2024/guillermin-m2

- https://gricad-gitlab.univ-grenoble-alpes.fr/legi/post-doc/2024/2024-postdoc-agoua-wesley

- http://intranet.legi.grenoble-inp.fr/ (avec liens vers wiki, réservation salles, webmail)

- https://foss.heptapod.net/fluiddyn/fluidsim

- https://foss.heptapod.net/fluiddyn/fluiddyn_papers

- MR Kolmo law ns3d: https://foss.heptapod.net/fluiddyn/fluidsim/-/merge_requests/298

- https://foss.heptapod.net/fluiddyn/fluidsim/-/tree/branch/default/doc/examples/forcing_anisotropic_3d/toro2022

- https://foss.heptapod.net/fluiddyn/fluidsim/-/blob/branch/default/doc/examples/simul_ns3d_forced_isotropic.py

- The supercomputer: https://foss.heptapod.net/fluiddyn/fluidsim/-/tree/branch/default/doc/examples/clusters/gricad
