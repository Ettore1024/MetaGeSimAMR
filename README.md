# CAMISIM (new) 'known distribution' modality

https://img.shields.io/badge/<Python>-<v3.9>-<informational>

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

On the other hand, the new modality of CAMISIM (**known distribution**) may be used also outside the **Snakemake pipeline**, but, in that case, an extra input file
(described [here](https://github.com/Ettore1024/MetaGeSim-AMR#the-new-file-of-abundances)) and three new parameters in the configuration file 
(described [here](https://github.com/Ettore1024/MetaGeSim-AMR#the-new-configuration-file-parameters)) are required. 

An in-depth description is proposed in the following sections.

### The aim of the known distribution modality:
The **known distribution** modality is a solution to the lack of a metagenomic simulation involving an _a priori_ known distribution of the microbial population, _when_ it is 
also useful to simulate (synthetic) strains.

It is worth pointing out that the original version of CAMISIM may work in two different modes, the so-called _from profile_ and _de novo_. In the _from profile_ mode, the user gives in input a file 
with the population distribution, but no strain is generated during the simulation; on the other hand, the _de novo_ mode is based on the creation of new strains (through a
tool called [sgEvolver](https://darlinglab.org/mauve/developer-guide/benchmarking.html)), but the population distribution is randomly generated starting from a log-normal distribution 
(further details may be found [here](https://github.com/CAMI-challenge/CAMISIM/wiki/Distribution-of-genomes)).

Thus, the **known distribution** modality proposes a way to combine these two different approaches.

The **known distribution** modality is a (sub-)mode of the _de novo_ one. The idea behind it is just to change the way in which the population distribution is generated. 
The four original modality of CAMISIM in the _de novo_ mode are _differential_, _replicates_, _timeseries normal_, and _timeseries lognormal_. 
It is worth mentioning that they are all based on the log-normal distribution and they only affect the simulation of the population distribution for different samples.
This means that the user can not see the difference among those four modalities only looking to the results of the distribution of one sample (as described [here](https://github.com/CAMI-challenge/CAMISIM/wiki/Distribution-of-genomes)).

On the other hand, the **known distribution** modality works differently, since the simulation of the population distribution does not start with a sampling from the log-normal distribution; instead, 
it starts from the given relative abundances of the input genomes and then manipulates them through the **broken stick model**.

The idea behind the broken stick model is to divide the given input abundance of each genome, among its generated strains. This distribution of the original abundance among strains is 
based on the Beta distribution and it is further analyzed [here](https://github.com/Ettore1024/MetaGeSim-AMR#redistribution-of-abundances).

As already said, in order to work with this new modality CAMISIM needs a new input file and some changes in the configuration file. The next sections will delve into their description.  

### The new file of abundances:
The new input file must be a _tsv_ file with no header and two columns: the first one with the _genome_ID_ used in the other input files required by CAMISIM 
(_metadata.tsv_ and _genome_to_id.tsv_); the second one with the relative abundance of each original genome.

The configuration file's parameter _num_real_genomes_ must of course be set to a number equal to or smaller than the number of genomes that are available in input.
In the second case, the _abundance.tsv_ file can be filled in two different ways:

  1. The user can only list the genomes of interest, with their relative abundance, omitting all the other genomes;

  2. The user can list all the genomes given in input (inside the `genomes` folder, I will come back later on this point); in this case, all the genomes the user do not want to use 
during the simulation must be put at the bottom of the list and their relative abundance should be set to 0.

A clarification on point 2 should be highlighted: if the sum of the abundances of the considered genomes does not equal 1, the simulation will not stop and 
no error will emerge. This is consistent with the original _de novo_ modality: the relative abundances of each genome and each strain is always re-normalised so that their sum will be euqal to 1.
As a result, if the abundances given in input are not normalised to 1, the ouput ones will; thus, the relative proportions among genomes will be preserved.

Once the _abundance.tsv_ file is created, a new parameter must be considered in the configuration file, so that CAMISIM will access the file. This new parameter (as well as the other two related to the
mathematical simulation) will be described in the next section.
 
### The new configuration file parameters:

### Snakemake pipeline:

### The input_file_preparation script:

## Testing

## Additional clarifications

### Redistribution of abundances:

### Example of configuration file:

# What's new in the scripts

# References
[1] Fritz, A. Hofmann, P. et al, **CAMISIM: Simulating metagenomes and microbial communities**, _Microbiome_, 2019, 7:17, doi: [10.1186/s40168-019-0633-6](https://doi.org/10.1186/s40168-019-0633-6), github: [CAMI-challenge/CAMISIM](https://github.com/CAMI-challenge/CAMISIM)

[2] _National Center for Biotechnology Information_, **NCBI** [www.ncbi.nlm.nih.gov](https://www.ncbi.nlm.nih.gov/)

[3] _Pathosystems Resource Integration Center_, **PATRIC** [patricbrc.org](https://patricbrc.org/) 

[4] _Bacterial and Viral Bioinformatics Resource Center_,  **BV-BRC** [bv-brc.org](https://www.bv-brc.org/)


