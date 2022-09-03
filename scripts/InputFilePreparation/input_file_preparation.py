import csv
import json
from configparser import ConfigParser

def dictionary_definition_for_amr ():
	"""
		Comment here
	"""

	dict_of_columns = {
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

	return dict_of_columns


def read_and_store_tsv_input (input_tsv_path, dict_of_columns):
	"""
		Comment here
	"""

	with open(input_tsv_path, 'r') as input_tsv:
		read_input_tsv = csv.reader(input_tsv, delimiter = '\t')
		next(read_input_tsv, None)

		for row in read_input_tsv:
			dict_of_columns[genome_IDs].append(row[0])
			dict_of_columns[species].append(row[1])
			dict_of_columns[abundances].append(row[2])
			dict_of_columns[patric_IDs].append(row[3])
			dict_of_columns[antibiotics].append(row[4])
			dict_of_columns[phenotypes].append(row[5])
			dict_of_columns[genome_lengths].append(row[6])
			dict_of_columns[novelty_cats].append(row[7])
			dict_of_columns[genome_filenames].append(row[8])

	return dict_of_columns

def read_and_store_json_input (input_json_path):
	"""
		Comment here
	"""

	with open(input_json_path, 'r') as input_json:
		json_to_dict = json.load(input_json)

	simulation_dir = json_to_dict['simulation_directory']

	return [json_to_dict, simulation_dir]


def wrt_abundance_file (abundance_path, dict_of_columns):
	"""
		Comment here
	"""

	with open(abundance_path, 'w') as abundance_file:
		wrt_abundance = csv.writer(abundance_file, delimiter = '\t')
		for index in range(len(dict_of_columns['genome_IDs'])):
			wrt_abundance.writerow([dict_of_columns['genome_IDs'][index], dict_of_columns['abundances'][index]])


def wrt_metadata_file (metadata_path, dict_of_columns):
	"""
		Comment here
	"""

	with open(metadata_path, 'w') as metadata_file:
		wrt_metadata = csv.writer(metadata_file, delimiter = '\t')
		wrt_metadata.writerow(['genome_ID', 'OTU', 'NCBI_ID', 'novelty_category'])
		for index in range(len(dict_of_columns['genome_IDs'])):
			wrt_metadata.writerow([dict_of_columns['genome_IDs'][index],
                                               str(index+1),
                                               str(int(float(dict_of_columns['patric_IDs'][index]))),
                                               dict_of_columns['novelty_cats'][index]])


def wrt_genome_to_id_file (genome_to_id_path, dict_of_columns, simul_dir):
	"""
		Comment here
	"""

	with open(genome_to_id_path, 'w') as genome_to_id_file:
		wrt_genome_to_id = csv.writer(genome_to_id_file, delimiter = '\t')

		for index in range(len(dict_of_columns['genome_IDs'])):
			wrt_genome_to_id.writerow([dict_of_columns['genome_IDs'][index],
                                                   str(simul_dir+'/genomes/'+dict_of_columns['genome_filenames'][index])


def config_definition (configuration_file):
	"""
		Comment here
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
		'readsim': '',
		'error_profiles': '',
		'samtools': '',
		'profile': 'mbarc',
		'size': '',
		'type': 'art',
		'fragments_size_mean': '',
		'fragment_size_standard_deviation': ''
	}

	configuration_file['CommunityDesign'] = {
		'ncbi_taxdump': '',
		'strain_simulation_template': '',
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
		'input_genomes_to_zero': 'True',
		'log_mu': '1',
		'log_sigma': '2',
		'gauss_mu': '1',
		'gauss_sigma': '1',
		'view': 'False'
	}

	return configuration_file


def config_settings (config, dict_json, dict_of_columns, metadata_path, genome_to_id_path, abundance_path):
	"""
		Comment here
	"""

	config.set('Main', 'max_processor', dict_json['max_processor'])
	config.set('Main', 'seed', dict_json['seed'])
	config.set('Main', 'output_directory', dict_json['output_directory'])
	config.set('ReadSimulator', 'size', dict_json['size'])
	config.set('ReadSimulator', 'fragments_size_mean', dict_json['fragm_size_mean'])
	config.set('ReadSimulator', 'fragment_size_standard_deviation', dict_json['fragm_size_std_dev'])
	config.set('CommunityDesign', 'number_of_samples', dict_json['number_of_samples'])
	config.set('community0', 'metadata', metadata_path)
	config.set('community0', 'id_to_genome_file', genome_to_id_path)
	config.set('community0', 'path_to_abundance_file', abundance_path)
	config.set('community0', 'genomes_total', dict_json['genomes_total'])
	config.set('community0', 'num_real_genomes', str(len(dict_of_columns['genome_IDs'])))
	config.set('community0', 'equally_distributed_strains', dict_json['equally_distributed_strains'])

	return config_file


def wrt_config_file (config_path, config):
	"""
		Comment here
	"""

	with open(config_path, 'w') as config_file:
		config.write(config_file)


def wrt_genomes_info_file (genomes_info_path, dict_of_columns, input_tsv_path)
	"""
		Comment here
	"""

	dict_from_tsv = {}
	for index in range(len(dict_of_columns['genome_IDs'])):
		dict_from_tsv[dict_of_columns['genome_IDs'][index]] = {}

	with open(input_tsv_path, 'r') as input_tsv:
		input_tsv_reader = csv.DictReader(input_tsv, delimiter = '\t')
		i = 0
		for row in input_tsv_reader:
			dict_from_tsv[dict_of_columns['genome_IDs'][i]].update(dict(row))
			i += 1

	keys_list = ['Genome_ID', 'Novelty_category']
	for index in range(len(dict_of_columns['genome_IDs'])):
		for key in keys_list:
			try:
				del dict_from_tsv[dict_of_columns['genome_IDs'][index]][key]
			except KeyError:
				pass

	with open(genomes_info_path, 'w') as genomes_info_file:
		json.dump(dict_from_tsv, genomes_info_file, indent = 8)
