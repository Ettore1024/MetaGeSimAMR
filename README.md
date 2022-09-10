# CAMISIM (new) 'known distribution' modality

## Why this new modality
The modality called **known distribution** is built starting from the _de novo_ mode of [CAMISIM](https://github.com/CAMI-challenge/CAMISIM).
In the **known distribution** modality, as well as in all the other already available modalities in CAMISIM, new strains can be generated through sgEvolver.

What this new modality does differently is the community design step, which, in this case, is based on a distribution given, in input, by the user, and not randomly generated 
from a log-normal distribution (that is what happens in the four original modalities of CAMISIM).

Once the new strains are generated, this new modality will distribute the relative abundances of each "original" genome to all its simulated strains. An example of this process 
can be found in the [here](https://github.com/Ettore1024/Metagenomic_known_distribution/#Redistribution-of-abundances).

In this repository you can find the new version of the CAMISIM tool, in which the above-described extra modality in the _de novo_ mode is implemented. A Snakefile is presented, too;
it allows to define a simple pipeline which was used for Antimicrobial Resistance (AMR) studies, for the synthetic data generation step.

The combination of these two pieces of scripts forms the MetaGeSim-AMR tool, a MetaGenomic Simulation tool suited for AMR studies.

# Installation
For the installation, you may simply launch the following command:

    git clone https://github.com/Ettore1024/MetaGeSim-AMR.git

In this way, both the new version of CAMISIM and the Snakemake pipeline, which compose the MetaGeSim-AMR tool, will be installed.

## Dependencies
In order to properly work, the MetaGeSim-AMR tool needs some dependencies to be installed. The list of dependencies for CAMISIM can be found [here](https://github.com/CAMI-challenge/CAMISIM/wiki/User-manual#dependencies).  
To be more precise, the conda-installable dependencies (BIOM, Biopython, Numpy, Matplotlib) are not required to be manually installed by the user when working with the Snakemake pipeline, since a
conda environment is internally set up when launching the pipeline; the characteristics of the environment can be found in [camisim_env.yaml](https://github.com/Ettore1024/MetaGeSim-AMR/blob/main/camisim_env.yaml).

All the other dependencies ([Perl 5](https://www.perl.org/), [wgsim](https://github.com/lh3/wgsim), [NanoSim](https://github.com/abremges/NanoSim), 
[PBsim](https://github.com/pfaucon/PBSIM-PacBio-Simulator), [SAMtools 1.0](http://www.htslib.org/)) may be installed following the instructions presented in each site. 

# Documentation
A complete documentation for the original CAMISIM tool can be found [here](https://github.com/CAMI-challenge/CAMISIM/wiki/User-manual).

The following sections will be about the new **known distribution** modality, together with its features and options, and the Snakemake pipeline.

## How to use the tool

### The aim of the **known distribution** modality

### The new file of abundances

### The new configuration file parameters

## Redistribution of abundances

## Other minor differences from the original CAMISIM tool
 
