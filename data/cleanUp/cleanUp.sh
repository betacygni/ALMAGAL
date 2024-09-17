#!/bin/bash

# Clean-up files in the ../mpi-runs directory
# Use only with caution!
#
echo "Delete mpi-out files (may take time)"
rm ../mpi-runs/mpi-out.*
echo "Delete mpi-err files (may take time)"
rm ../mpi-runs/mpi-err.*
for i in ../mpi-runs/*; do
    if ! grep -qxFe "$i" basic_files.txt; then
        echo "Deleting: $i"
        rm -rf "$i"
    fi
done
