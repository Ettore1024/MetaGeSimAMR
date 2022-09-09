__author__ = "Ettore Rocchi"

"""
	This script defines some functions which test if the functions
	defined by Ettore Rocchi in input_file_preparation.py and in
	populationdistribution.py work properly
"""

import pytest
import csv
from scripts.PopulationDistribution.populationdistribution import PopulationDistribution
from scripts.InputFilePreparation.input_file_preparation import *


tsv_path = "./input_population/input.tsv"


def test_Broken_stick_model_for_one_strain():

	genome_ID = 'First_genome'
	total_genomes_dict = {'First_genome': 0.7, 'Second_genome': 0.3, 'simulated_First_genome_Taxon001': 0}
	original_genome_abundance = total_genomes_dict[genome_ID]
	number_strains = 1

	input_genomes_to_zero = True
	dict = PopulationDistribution.Broken_stick_model(genome_ID, total_genomes_dict, original_genome_abundance, number_strains, input_genomes_to_zero)

	assert dict['simulated_First_genome_Taxon001'] == 0.7

	input_genomes_to_zero = False
	dict = PopulationDistribution.Broken_stick_model(genome_ID, total_genomes_dict, original_genome_abundance, number_strains, input_genomes_to_zero)

	assert dict['simulated_First_genome_Taxon001'] + dict['First_genome'] == 0.7

def test_tsv_input_columns():

	dict = read_and_store_tsv_input(tsv_path)

	with open(tsv_path, 'r') as tsv_file:
		tsv_reader = csv.reader(tsv_file, delimiter = '\t')
		num_columns = len(list(tsv_reader)[0])

	assert len(dict) == num_columns

def test_tsv_rows_have_same_number_of_elements():

	dict_length = len(read_and_store_tsv_input(tsv_path))

	with open(tsv_path, 'r') as tsv_file:
		for row in csv.reader(tsv_file, delimiter = '\t'):
			assert len(row) == dict_length

