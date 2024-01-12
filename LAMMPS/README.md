## This folder contains sample scripts for LAMMPS inputs
See `ACAJIZ` and `ASEJOZ01_clean`, which contains the LAMMPS input scripts for MD simulations of thermal expansion and the python analysis scripts.

Under each folder, the results of the `MD` runs are collected in `MOF_Cofficient.csv` and the linear-fit of `V` vs `T` can be visualized in `Validation.png`.
The input files for `LAMMPS`: `data.MOF` and `in.lammps` are provided in the `input` subfolder respectively.

Also, note that the regression fitting here are collected for 100K ~ 500K in intervals of 50K. To facilitate faster screening, we used interval of 100K over the same temperature range.
