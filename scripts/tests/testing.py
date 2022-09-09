__author__ = "Ettore Rocchi"

"""
	This script defines some functions which test if the functions
	defined by Ettore Rocchi in input_file_preparation.py and in
	populationdistribution.py work properly
"""


     #######################
     #    Preliminaries    #
     #######################

import pytest
import csv
import math
import numpy as np
import pathlib
from configparser import ConfigParser
from scripts.PopulationDistribution.populationdistribution import PopulationDistribution
from scripts.InputFilePreparation.input_file_preparation import *


tsv_path = "./input_population/input.tsv"
json_path = "./input_population/input.json"

config_path = "./input_population/config.ini"
abundance_path = "./input_population/abundance.tsv"
metadata_path = "./input_population/metadata.tsv"
genome_to_id_path = "./input_population/genome_to_id.tsv"
simulation_dir = "./input_population"


def is_float(string):
	try:
		float(string)
		return True
	except ValueError:
		return False

def is_integer(string):
	try:
		int(string)
		return True
	except ValueError:
		return False

def is_bool(string):
	try:
		bool(string)
		return True
	except ValueError:
		return False


     #######################
     #        Tests        #
     #######################

def test_Broken_stick_model_distributes_abundance_properly_input_genome_to_zero():
	"""
		Comment here
	"""

	genome_ID = 'First_genome'
	total_genomes_dict = {'First_genome': 0.7, 'Second_genome': 0.3, 'simulated_First_genome.Taxon001': 0, 'simulated_First_genome.Taxon002': 0}
	original_genome_abundance = total_genomes_dict[genome_ID]
	number_strains = 2
	original_dict = total_genomes_dict.copy()

	input_genomes_to_zero = True
	dict = PopulationDistribution.Broken_stick_model(genome_ID, total_genomes_dict, original_genome_abundance, number_strains, input_genomes_to_zero)

	assert math.isclose(dict['simulated_First_genome.Taxon001'] + dict['simulated_First_genome.Taxon002'], original_dict['First_genome'], abs_tol = 0.00001)


def test_Broken_stick_model_distributes_abundance_properly():
	"""
		Comment here
	"""

	genome_ID = 'First_genome'
	total_genomes_dict = {'First_genome': 0.7, 'Second_genome': 0.3, 'simulated_First_genome.Taxon001': 0, 'simulated_First_genome.Taxon002': 0}
	original_genome_abundance = total_genomes_dict[genome_ID]
	number_strains = 2
	original_dict = total_genomes_dict.copy()

	input_genomes_to_zero = False
	dict = PopulationDistribution.Broken_stick_model(genome_ID, total_genomes_dict, original_genome_abundance, number_strains, input_genomes_to_zero)

	assert math.isclose(dict['simulated_First_genome.Taxon001'] + dict['simulated_First_genome.Taxon002'] + dict['First_genome'], original_dict['First_genome'], abs_tol = 0.00001)


def test_abundances_input_equal_to_distributed_abundances():


	total_genomes_dict = {'E.coli': 0.5, 'S.Aureus': 0.3, 'S.pneumoniae': 0.2, 'simulated_E.coli.Taxon001': 0, 'simulated_S.aureus.Taxon002': 0, 'simulated_S.pneumoniae.Taxon003': 0}
	total_abundances_input = sum(total_genomes_dict[key] for key in total_genomes_dict)

	np.random.seed(42)
	number_of_samples = np.random.randint(1, 10)
	population_list = [[0.0] * number_of_samples for _ in range(len(total_genomes_dict))]
	list_of_genome_id = [key for key in total_genomes_dict]
	input_genomes_to_zero = bool(np.random.randint(0, 1))

	dict_of_tsv_columns = read_and_store_tsv_input(tsv_path)
	wrt_abundance_file(abundance_path, dict_of_tsv_columns)

	distribution = PopulationDistribution()
	distribution.distribute_abundance_to_strains(population_list, number_of_samples, abundance_path, list_of_genome_id, input_genomes_to_zero)

	abundance_file = pathlib.Path(abundance_path)
	abundance_file.unlink()

	distributed_abundances = [0 for _ in range(number_of_samples)]
	for i in range(number_of_samples):
		for j in range(len(total_genomes_dict)):
			distributed_abundances[i] += population_list[j][i]
		assert math.isclose(total_abundances_input, distributed_abundances[i], abs_tol = 0.00001)


def test_genomes_total_greater_or_equal_to_input_genomes():

	dict = read_and_store_tsv_input(tsv_path)

	with open(tsv_path, 'r') as tsv_file:
		tsv_reader = csv.reader(tsv_file, delimiter = '\t')
		next(tsv_reader, None)
		num_rows = sum(1 for row in tsv_reader)

	with open(json_path, 'r') as json_file:
		json_dict = json.load(json_file)

	total_num_genomes = int(json_dict['genomes_total'])

	assert  total_num_genomes >= num_rows


def test_tsv_rows_have_same_number_of_elements():

	dict_length = len(read_and_store_tsv_input(tsv_path))

	with open(tsv_path, 'r') as tsv_file:
		for row in csv.reader(tsv_file, delimiter = '\t'):
			assert len(row) == dict_length


def test_all_configs_are_set():

	config = ConfigParser()
	configuration_file_definition(config)

	tsv_dict = read_and_store_tsv_input(tsv_path)
	json_dict = read_and_store_json_input(json_path)

	configuration_file_settings(config, json_dict, tsv_dict, abundance_path, metadata_path, genome_to_id_path, simulation_dir)

	for section in config.sections():
		for key, value in config.items(section):
			if not key == 'id_to_gff_file':
				assert value != ''


def test_tsv_values_have_correct_types():

	tsv_dict = read_and_store_tsv_input(tsv_path)

	for key in tsv_dict:
		assert isinstance(tsv_dict[key], list)

	for i in range(len(tsv_dict['genome_IDs'])):
		assert isinstance(tsv_dict['genome_IDs'][i], str)
		assert tsv_dict['genome_IDs'][i] != ''
		assert isinstance(tsv_dict['species'][i], str)
		assert tsv_dict['species'][i] != ''
		assert is_float(tsv_dict['abundances'][i])
		assert (float(tsv_dict['abundances'][i]) <= 1 and float(tsv_dict['abundances'][i]) >= 0)
		assert is_float(tsv_dict['patric_IDs'][i])
		assert isinstance(tsv_dict['antibiotics'][i], str)
		assert tsv_dict['phenotypes'][i] in ["Resistant", "resistant", "Susceptible", "susceptible", "Intermediate", "intermediate"]
		assert is_integer(tsv_dict['genome_lengths'][i])
		assert tsv_dict['novelty_cats'][i] in ["known_strain", "known_genus", "known_family"] #attention!
		assert isinstance(tsv_dict['genome_filenames'][i], str)


def test_json_values_have_correct_types():

	json_dict = read_and_store_json_input(json_path)

	for key in json_dict:
		assert json_dict[key] != ""

	assert is_integer(json_dict["seed"])
	assert is_integer(json_dict["max_processor"])
	assert int(json_dict["max_processor"]) > 0
	assert is_float(json_dict["size"])
	assert is_integer(json_dict["fragm_size_mean"])
	assert is_integer(json_dict["fragm_size_std_dev"])
	assert is_integer(json_dict["number_of_samples"])
	assert int(json_dict["number_of_samples"]) > 0
	assert is_bool(json_dict["equally_distributed_strains"])
	assert is_bool(json_dict["input_genomes_to_zero"])
	assert is_integer(json_dict["genomes_total"])
	assert int(json_dict["genomes_total"]) > 0

