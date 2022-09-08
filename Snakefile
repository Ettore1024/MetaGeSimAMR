__author__ = "Ettore Rocchi"


rule camisim_pipeline:
	"""
		This rule launch the CAMISIM simulation.

		Input:
			- config_in: the configuration file of the
				     CAMISIM simulation

		Output:
			- out: directory of output where the simulated reads can
			       can be found
	"""

	input:
		config_in = "{population}/config.ini"

	output:
		out = directory("{population}/out")		

	conda: "camisim_env.yaml"

	threads: 32
	
	shell:
		"""
			rm -rf {wildcards.population}/out/
			python metagenomesimulation.py {input.config_in}
		"""

rule population_input_files:
	"""
		This rule creates the config.ini file if it does not exist.
		Together with it other four files are created through the functions
		defined in input_file_preparation.py

		Three of the other four files are required for launching the CAMISIM
		simulation; the last file is a sum up of the genomes' information.

		Input:
			- in_1: input.tsv file with genomes' information
			- in_2: input.json file with configuration settings

		Output:
			- out: config.ini file of the CAMISIM simulation
	"""

	input:	
		in_1 = "{population}/input.tsv",
		in_2 = "{population}/input.json"

	output:
		out = "{population}/config.ini"

	shell:
		"""
			python scripts/InputFilePreparation/input_file_preparation.py {wildcards.population}
		"""
