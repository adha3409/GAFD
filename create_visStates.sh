#!/bin/bash
# this file creates QuICC visState* files from a sequence of state files

for f in state0*
    do
       echo "Processing $f file.."	
       ln -sf $f state4Visu.hdf5
       extract=${f:5:4} 
       mpirun -n 8 Executables/BoussinesqPlaneRBCVisu
       cp visState0000.hdf5 visState$extract.hdf5
    done
