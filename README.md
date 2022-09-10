# CAMISIM (new) 'known distribution' modality

## Why this new modality
The modality called **known distribution** is built starting from the _de novo_ mode of [CAMISIM](https://github.com/CAMI-challenge/CAMISIM).
In the **known distribution** modality, as well as in all the other already available modalities in CAMISIM, new strains can be generated through sgEvolver.

What this new modality does differently is the community design step, which, in this case, is based on a distribution given, in input, by the user, and not randomly generated 
from a log-normal distribution (that is what happens in the four original modalities of CAMISIM).

Once the new strains are generated, this new modality will distribute the relative abundances of each "original" genome to all its simulated strains. An example of this process 
can be found in the [here](https://github.com/Ettore1024/MetaGeSim-AMR#redistribution-of-abundances).

In this repository you can find the new version of the CAMISIM tool, in which the above-described extra modality in the _de novo_ mode is implemented. A **Snakefile** is presented, too;
it allows to define a simple pipeline which was used for Antimicrobial Resistance (AMR) studies, for the synthetic data generation step.

The combination of these two pieces of scripts forms the **MetaGeSim-AMR** tool, a MetaGenomic Simulation tool suited for AMR studies.

# Installation
For the installation, you may simply launch the following command:

    git clone https://github.com/Ettore1024/MetaGeSim-AMR.git

In this way, both the new version of CAMISIM and the Snakemake pipeline, which compose the **MetaGeSim-AMR** tool, will be installed.

## Dependencies
In order to properly work, the **MetaGeSim-AMR** tool needs some dependencies to be installed. The list of dependencies for CAMISIM can be found [here](https://github.com/CAMI-challenge/CAMISIM/wiki/User-manual#dependencies).  
To be more precise, the conda-installable dependencies ([BIOM](https://pypi.org/project/biom-format/), [Biopython](https://biopython.org/), 
[Numpy](https://numpy.org/), [Matplotlib](https://matplotlib.org/)) are not required to be manually installed by the user when working with the **Snakemake pipeline**, since a
conda environment is internally set up when launching the pipeline; the characteristics of the environment can be found in [camisim_env.yaml](https://github.com/Ettore1024/MetaGeSim-AMR/blob/main/camisim_env.yaml).

All the other dependencies ([Perl 5](https://www.perl.org/), [wgsim](https://github.com/lh3/wgsim), [NanoSim](https://github.com/abremges/NanoSim), 
[PBsim](https://github.com/pfaucon/PBSIM-PacBio-Simulator), [SAMtools 1.0](http://www.htslib.org/)) may be installed following the instructions presented in each site. 

# Documentation
A complete documentation for the original CAMISIM tool can be found [here](https://github.com/CAMI-challenge/CAMISIM/wiki/User-manual).

The following sections will be about the new **known distribution** modality, together with its features and options, and the **Snakemake pipeline**.

## How to use the tool
The **MetaGeSim-AMR** tool allows to generate metagenomic synthetic data only starting from two input files (_input.tsv_ and _input.json_).
In order to this, the **Snakemake pipeline** must be used (see [here](https://github.com/Ettore1024/MetaGeSim-AMR#snakemake-pipeline)).

On the other hand, the new modality of CAMISIM (**known distribution**) may be used also outside the Snakemake pipeline, but, in that case, an extra input file
(described [here](https://github.com/Ettore1024/MetaGeSim-AMR#the-new-file-of-abundances)) and three new parameters in the configuration file 
(described [here](https://github.com/Ettore1024/MetaGeSim-AMR#the-new-configuration-file-parameters)) are required. 

An in-depth description is proposed in the following sections.

### The aim of the known distribution modality:
The **known distribution** modality is a solution to the lack of a metagenomic simulation involving an _a priori_ known distribution of the microbial population, **when** it is 
also useful to simulate (synthetic) strains.

It is worth pointing out that CAMISIM may work in two different modes, the so-called _from profile_ and _de novo_. In the _from profile_ mode, the user gives in input a file 
with the population distribution, but no strain is generated during the simulation; on the other hand, the _de novo_ mode is based on the creation of new strains (through a
tool called sgEvolver), but the population distribution is randomly generated starting from a log-normal distribution (further details may be found [here](https://github.com/CAMI-challenge/CAMISIM/wiki/Distribution-of-genomes)).

Thus, the **known distribution** modality proposes a way to combine these two different approaches.

### The new file of abundances:

### The new configuration file parameters:

### Snakemake pipeline:

### The input_file_preparation script:

## Testing

# Additional clarifications

## Redistribution of abundances

## Example of configuration file

## Other minor differences from the original CAMISIM tool

# References
[1] Fritz, A. Hofmann, P. et al, **CAMISIM: Simulating metagenomes and microbial communities**, _Microbiome_, 2019, 7:17, doi: [10.1186/s40168-019-0633-6](https://doi.org/10.1186/s40168-019-0633-6), github: [CAMI-challenge/CAMISIM](https://github.com/CAMI-challenge/CAMISIM)

[2] _National Center for Biotechnology Information_, **NCBI** [www.ncbi.nlm.nih.gov](https://www.ncbi.nlm.nih.gov/)

[3] _Pathosystems Resource Integration Center_, **PATRIC** [patricbrc.org](https://patricbrc.org/) 

[4] _Bacterial and Viral Bioinformatics Resource Center_,  **BV-BRC** [bv-brc.org](https://www.bv-brc.org/)


