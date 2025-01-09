# Isotropic tests scripts
In this folder we regroup the content of the [folder of Wesley Agoua about isotropic tests](https://gricad-gitlab.univ-grenoble-alpes.fr/legi/post-doc/2024/2024-postdoc-agoua-wesley/-/tree/main/test_iso) with modifications so that it can be used during this project.

## Computing setup 
Don't forget to execute `source /applis/site/guix-start.sh` when logging in on Dahu!

### Dahu Cluster (With Guix)
We try to use the Guix configuration to submit our job but it doesn't work now.

Submit job with 
```sh
python Guix_Dahu_submit_iso3D.py
```

### Dahu Cluster (With Miniconda)
We can submit job on Dahu without using Guix by using a conda env

Submit job with
```sh
./Dahu_submit_iso3D.py
```

### Zen Cluster
Because I have access to Mesonet server for my academic year, I tried to submit job on this cluster also.

Submit job with
```sh
./Zen_submit_iso3D.py
```