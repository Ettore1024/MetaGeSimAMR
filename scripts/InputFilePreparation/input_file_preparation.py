#!/usr/bin/env python

"""
	The script implements the generation of CAMISIM's input files
	starting from two files containing interesting information
	for AMR studies
"""

__author__ = "Ettore Rocchi"

import csv
import json
import sys
from pathlib import Path
from configparser import ConfigParser

def read_and_store_tsv_input (input_tsv_path):
	"""
		This function reads the input.tsv file and stores the information
		in a dictionary.

		Parameters:
			- input_tsv_path: (string) absolute path of input.tsv

		Output:
			- tsv_columns_dict: (dictionary) each key contains a list
					    of values, each one associated to a
					    different input genome
	"""

	tsv_columns_dict = {
                        'genome_IDs' : [],
                        'species' : [],
                        'abundances' : [],
                        'patric_IDs' : [],
                        'antibiotics' : [],
                        'phenotypes' : [],
                        'genome_lengths' : [],
                        'novelty_cats' : [],
                        'genome_filenames' : []
			}

	with open(input_tsv_path, 'r') as input_tsv:
		read_input_tsv = csv.reader(input_tsv, delimiter = '\t')
		next(read_input_tsv, None)

		for row in read_input_tsv:
			tsv_columns_dict['genome_IDs'].append(row[0])
			tsv_columns_dict['species'].append(row[1])
			tsv_columns_dict['abundances'].append(row[2])
			tsv_columns_dict['patric_IDs'].append(row[3])
			tsv_columns_dict['antibiotics'].append(row[4])
			tsv_columns_dict['phenotypes'].append(row[5])
			tsv_columns_dict['genome_lengths'].append(row[6])
			tsv_columns_dict['novelty_cats'].append(row[7])
			tsv_columns_dict['genome_filenames'].append(row[8])

	return tsv_columns_dict


def read_and_store_json_input (input_json_path):
	"""
		This function reads the input.json file and stores the information
		in a dictionary.

		Parameters:
			- input_json_path: (string) absolute path of input.json

		Output:
			- json_to_dict: (dictionary) each key is a configuration file
					setting
	"""

	with open(input_json_path, 'r') as input_json:
		json_to_dict = json.load(input_json)

	return json_to_dict


def wrt_abundance_file (abundance_path, dict_tsv_columns):
	"""
		This function writes the abundance.tsv file starting from the information
		taken from input.tsv

		Parameters:
			- abundance_path: (string) absolute path of abundance.tsv
					  (it doesn't need to exist)
			- dict_tsv_columns: (dictionary) it contains the information
					    stored by the read_and_store_tsv_input
					    function

		Output:
			No output is returned, but the abundance.tsv file is written
	"""

	with open(abundance_path, 'w') as abundance_file:
		wrt_abundance = csv.writer(abundance_file, delimiter = '\t')
		for index in range(len(dict_tsv_columns['genome_IDs'])):
			wrt_abundance.writerow([dict_tsv_columns['genome_IDs'][index], dict_tsv_columns['abundances'][index]])


def wrt_metadata_file (metadata_path, dict_tsv_columns):
	"""
		This function writes the metadata.tsv file starting from the information
		taken from input.tsv

		Parameters:
			- metadata_path: (string) absolute path of metadata.tsv
					 (it doesn't need to exist)
			- dict_tsv_columns: (dictionary) it contains the information
					    stored by the read_and_store_tsv_input
					    function

		Output:
			No output is returned, but the metadata.tsv file is written
	"""

	with open(metadata_path, 'w') as metadata_file:
		wrt_metadata = csv.writer(metadata_file, delimiter = '\t')
		wrt_metadata.writerow(['genome_ID', 'OTU', 'NCBI_ID', 'novelty_category'])
		for index in range(len(dict_tsv_columns['genome_IDs'])):
			wrt_metadata.writerow([dict_tsv_columns['genome_IDs'][index],
                                               str(index+1),
                                               str(int(float(dict_tsv_columns['patric_IDs'][index]))),
                                               dict_tsv_columns['novelty_cats'][index]])


def wrt_genome_to_id_file (genome_to_id_path, dict_tsv_columns, simul_dir):
	"""
		This function writes the genome_to_id.tsv file starting from the information
		taken from input.tsv

		Parameters:
			- genome_to_id_path: (string) absolute path of genome_to_id.tsv
					     (it doesn't need to exist)
			- dict_tsv_columns: (dictionary) it contains the information
					    stored by the read_and_store_tsv_input
					    function

		Output:
			No output is returned, but the genome_to_id.tsv file is written
	"""

	with open(genome_to_id_path, 'w') as genome_to_id_file:
		wrt_genome_to_id = csv.writer(genome_to_id_file, delimiter = '\t')
		for index in range(len(dict_tsv_columns['genome_IDs'])):
			wrt_genome_to_id.writerow([dict_tsv_columns['genome_IDs'][index],
                                                   str(simul_dir+'/genomes/'+dict_tsv_columns['genome_filenames'][index])])


def configuration_file_definition (configuration_file):
	"""
		This function defines the sections and the parameters required by CAMISIM
		to launch the simulation.

		Some of the parameters are already set here (some of them to help the user,
		when the parameter is not crucial, others because the considered AMR study
		requires precise settings).

		What's new?
			W.r.t the original version of CAMISIM there are three new parameters:
			- path_to_abundance_file: (string) absolute path of abundance.tsv
			- equally_distributed_strains: (bool) it decides if the number of generated
						       strains will be equally distributed among
						       the original genomes or not
			- input_genomes_to_zero: (bool) it decides if the input genomes' abundances
						 will be totally re-distributed among the strains
						 or not

		Parameters:
			- configuration_file: (ConfigParser) this object will be updated
					      inside this function

		Output:
			No output is returned, but the ConfigParser object is updated
	"""

	configuration_file['Main'] = {
                'seed': '',
                'phase': '0',
                'max_processor': '',
                'dataset_id': 'RL',
                'output_directory': '',
                'temp_directory': '/tmp',
                'gsa': 'False',
                'pooled_gsa': 'False',
                'anonymous': 'False',
                'compress': '1'
	}

	configuration_file['ReadSimulator'] = {
                'readsim': 'tools/art_illumina-2.3.6/art_illumina',
                'error_profiles': 'tools/art_illumina-2.3.6/profiles',
                'samtools': 'tools/samtools-1.3/samtools',
                'profile': 'mbarc',
                'size': '',
                'type': 'art',
                'fragments_size_mean': '',
                'fragment_size_standard_deviation': ''
	}

	configuration_file['CommunityDesign'] = {
                'ncbi_taxdump': 'tools/ncbi-taxonomy_20170222.tar.gz',
                'strain_simulation_template': 'scripts/StrainSimulationWrapper/sgEvolver/simulation_dir',
                'number_of_samples': ''
	}

	configuration_file['community0'] = {
                'metadata': '',
                'id_to_genome_file': '',
                'id_to_gff_file': '',
                'path_to_abundance_file': '',
                'genomes_total': '',
                'num_real_genomes': '',
                'max_strains_per_otu': '1',
                'ratio': '1',
                'mode': 'known_distribution',
                'equally_distributed_strains': '',
                'input_genomes_to_zero': '',
                'log_mu': '1',
                'log_sigma': '2',
                'gauss_mu': '1',
                'gauss_sigma': '1',
                'view': 'False'
	}


def configuration_file_settings (configuration_file, dict_json, dict_tsv_columns, abundance_path, metadata_path, genome_to_id_path, simulation_directory):
	"""
		This function updates all the empty parameters of the configuration file,
		using the information taken from input.json and input.tsv

		Parameters:
			- configuration_file: (ConfigParser) this object will be updated
					      inside this function
			- dict_json: (dictionary) it contains the information stored by the
				     read_and_store_json_input function
			- dict_tsv_columns: (dictionary) it contains the information stored by
					    the read_and_store_tsv_input function
			- abundance_path: (string) absolute path of abundance.tsv
			- metadata_path: (string) absolute path of metadata.tsv
			- genome_to_id_path: (string) absolute path of genome_to_id.tsv
			- simulation_directory: (string) absolute path of the directory of the
						simulation

		Output:
			No output is returned, but the settings of the CongfigParser object
			are updated
	"""

	configuration_file.set('Main', 'max_processor', dict_json['max_processor'])
	configuration_file.set('Main', 'seed', dict_json['seed'])
	configuration_file.set('Main', 'output_directory', simulation_directory + '/out')
	configuration_file.set('ReadSimulator', 'size', dict_json['size'])
	configuration_file.set('ReadSimulator', 'fragments_size_mean', dict_json['fragm_size_mean'])
	configuration_file.set('ReadSimulator', 'fragment_size_standard_deviation', dict_json['fragm_size_std_dev'])
	configuration_file.set('CommunityDesign', 'number_of_samples', dict_json['number_of_samples'])
	configuration_file.set('community0', 'metadata', metadata_path)
	configuration_file.set('community0', 'id_to_genome_file', genome_to_id_path)
	configuration_file.set('community0', 'path_to_abundance_file', abundance_path)
	configuration_file.set('community0', 'genomes_total', dict_json['genomes_total'])
	configuration_file.set('community0', 'num_real_genomes', str(len(dict_tsv_columns['genome_IDs'])))
	configuration_file.set('community0', 'equally_distributed_strains', dict_json['equally_distributed_strains'])
	configuration_file.set('community0', 'input_genomes_to_zero', dict_json['input_genomes_to_zero'])


def wrt_configuration_file (configuration_file_path, configuration_file):
	"""
		This function writes the config.ini file starting from the information
		taken from input.json

		Parameters:
			- configuration_file_path: (string) absolute path of config.ini
						   (it doesn't need to exist)
			- configuration_file: (ConfigParser) this object contains all the
					      (already set) parameters which constitute the
					      configuration file

                Output:
                        No output is returned, but the config.ini file is written
	"""

	with open(configuration_file_path, 'w') as config_file:
		configuration_file.write(config_file)


def wrt_genomes_info_file (genomes_info_path, dict_tsv_columns, input_tsv_path):
	"""
		This function writes the genomes_info.json file starting from the information
		taken from input.tsv

		Parameters:
			- genomes_info_path: (string) absolute path of genomes_info.json
					     (it doesn't need to exist)
			- dict_tsv_columns: (dictionary) it contains the information
					    stored by the read_and_store_tsv_input function

                Output:
                        No output is returned, but the genomes_info.json file is written
	"""

	dict_from_tsv_info = {}
	for index in range(len(dict_tsv_columns['genome_IDs'])):
		dict_from_tsv_info[dict_tsv_columns['genome_IDs'][index]] = {}

	with open(input_tsv_path, 'r') as input_tsv:
		input_tsv_reader = csv.DictReader(input_tsv, delimiter = '\t')
		i = 0
		for row in input_tsv_reader:
			dict_from_tsv_info[dict_tsv_columns['genome_IDs'][i]].update(dict(row))
			i += 1

	keys_list = ['Genome_ID', 'Novelty_category']
	for index in range(len(dict_tsv_columns['genome_IDs'])):
		for key in keys_list:
			try:
				del dict_from_tsv_info[dict_of_columns['genome_IDs'][index]][key]
			except KeyError:
				pass

	with open(genomes_info_path, 'w') as genomes_info_file:
		json.dump(dict_from_tsv_info, genomes_info_file, indent = 8)


def amr_pipeline (directory_of_simulation):
	"""
		This function gathers all the above-defined functions and for this reason
		it represents the structure of the pipeline used for AMR studies.

		Parameters:
			- directory_of_simulation: (string) the absolute path for the directory of
						   simulation (containing input.tsv and input.json)

		Output:
			No output is returned, but five files are created:
				- abundance.tsv: file containing genome IDs and abundances
						 (no header)
				- metadata.tsv: file containing genome IDs, OTUs, NCBI IDs,
						novelty category (with header)
				- genome_to_id.tsv: file containing genome IDs and absolute paths
						    to their fasta file (no header)
				- config.ini: file with the settings required by CAMISIM to launch
					      the simulation
				- genomes_info.json: file with useful information about the original
						     genomes for AMR studies (e.g. Genome length,
						     antibiotic and associated phenotype [resistant/
						     susceptible], PATRIC ID)
	"""

	file_path_input_tsv = directory_of_simulation + '/input.tsv'
	dict_of_tsv_columns = read_and_store_tsv_input(file_path_input_tsv)

	file_path_input_json = directory_of_simulation + '/input.json'
	dict_of_json = read_and_store_json_input(file_path_input_json)

	file_path_abundance = directory_of_simulation + '/abundance.tsv'
	wrt_abundance_file(file_path_abundance, dict_of_tsv_columns)

	file_path_metadata = directory_of_simulation + '/metadata.tsv'
	wrt_metadata_file(file_path_metadata, dict_of_tsv_columns)

	file_path_genome_to_id = directory_of_simulation + '/genome_to_id.tsv'
	wrt_genome_to_id_file(file_path_genome_to_id, dict_of_tsv_columns, directory_of_simulation)

	config = ConfigParser()
	configuration_file_definition(config)
	configuration_file_settings(config, dict_of_json, dict_of_tsv_columns, file_path_abundance, file_path_metadata, file_path_genome_to_id, directory_of_simulation)
	file_path_config = directory_of_simulation + '/config.ini'
	wrt_configuration_file(file_path_config, config)

	file_path_genomes_info = directory_of_simulation + '/genomes_info.json'
	wrt_genomes_info_file(file_path_genomes_info, dict_of_tsv_columns, file_path_input_tsv)



if __name__ == "__main__":

	try:
		working_dir = sys.argv[1]
	except IndexError:
		sys.exit()

	working_dir_absolute_path = str(Path(working_dir).resolve())
	amr_pipeline(working_dir_absolute_path)
