# Code-Reuse-Estimation
Estimate similarities between binary files through analyzing symbol table output.

## Dependency Packages
* python (3.6)
* subprocess32 (3.2.7)
* pandas (0.20.1)
* os
* io
* sys

## How to run
### Try it out using included GNU core utilities by running:
`python3 binary_compare.py -r ../testecutables 10`
### One pair of executables
`python3 binary_compare.py <fullfilepath1> <fullfilepath2>`
### Directory of executables
`python3 binary_compare.py -r <directory> <number_of_comparisons>`
