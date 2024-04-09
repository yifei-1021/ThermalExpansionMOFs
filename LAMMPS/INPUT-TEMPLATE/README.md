This folder contains the simulation template for creating and running **LAMMPS** simulations for thermal expansion simulations for MOFs.

The Simulation input files can be created as follows:

1. Place the input (e.g., `in.ACAJIZ`) and data structure (`data.ACAJIZ`) file into a folder containing the `head.txt` and `tail.txt` in this folder
2. Run `spawn.sh` in bourne shell script. The `merge.py` should generate folders containing each structure input files for your
3. Run `LAMMPS` within each subfolder .
