import csv
import json
import sys
from pathlib import Path
from configparser import ConfigParser

def read_and_store_tsv_input (input_tsv_path):
	"""
		Comment here
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
		Comment here
	"""

	with open(input_json_path, 'r') as input_json:
		json_to_dict = json.load(input_json)

	return json_to_dict


def wrt_abundance_file (abundance_path, dict_tsv_columns):
	"""
		Comment here
	"""

	with open(abundance_path, 'w') as abundance_file:
		wrt_abundance = csv.writer(abundance_file, delimiter = '\t')
		for index in range(len(dict_tsv_columns['genome_IDs'])):
			wrt_abundance.writerow([dict_tsv_columns['genome_IDs'][index], dict_tsv_columns['abundances'][index]])


def wrt_metadata_file (metadata_path, dict_tsv_columns):
	"""
		Comment here
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
		Comment here
	"""

	with open(genome_to_id_path, 'w') as genome_to_id_file:
		wrt_genome_to_id = csv.writer(genome_to_id_file, delimiter = '\t')
		for index in range(len(dict_tsv_columns['genome_IDs'])):
			wrt_genome_to_id.writerow([dict_tsv_columns['genome_IDs'][index],
                                                   str(simul_dir+'/genomes/'+dict_tsv_columns['genome_filenames'][index])])


def configuration_file_definition (configuration_file):
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
                'input_genomes_to_zero': 'True',
                'log_mu': '1',
                'log_sigma': '2',
                'gauss_mu': '1',
                'gauss_sigma': '1',
                'view': 'False'
	}


def configuration_file_settings (configuration_file, dict_json, dict_of_columns, abundance_path, metadata_path, genome_to_id_path, simulation_directory):
	"""
		Comment here
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
	configuration_file.set('community0', 'num_real_genomes', str(len(dict_of_columns['genome_IDs'])))
	configuration_file.set('community0', 'equally_distributed_strains', dict_json['equally_distributed_strains'])


def wrt_configuration_file (configuration_file_path, configuration_file):
	"""
		Comment here
	"""

	with open(configuration_file_path, 'w') as config_file:
		configuration_file.write(config_file)


def wrt_genomes_info_file (genomes_info_path, dict_of_columns, input_tsv_path):
	"""
		Comment here
	"""

	dict_from_tsv_info = {}
	for index in range(len(dict_of_columns['genome_IDs'])):
		dict_from_tsv_info[dict_of_columns['genome_IDs'][index]] = {}

	with open(input_tsv_path, 'r') as input_tsv:
		input_tsv_reader = csv.DictReader(input_tsv, delimiter = '\t')
		i = 0
		for row in input_tsv_reader:
			dict_from_tsv_info[dict_of_columns['genome_IDs'][i]].update(dict(row))
			i += 1

	keys_list = ['Genome_ID', 'Novelty_category']
	for index in range(len(dict_of_columns['genome_IDs'])):
		for key in keys_list:
			try:
				del dict_from_tsv_info[dict_of_columns['genome_IDs'][index]][key]
			except KeyError:
				pass

	with open(genomes_info_path, 'w') as genomes_info_file:
		json.dump(dict_from_tsv_info, genomes_info_file, indent = 8)


def amr_pipeline (directory_of_simulation):
	"""
		Comment here
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
