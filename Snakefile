rule camisim_pipeline:
	"""
		Comment here
	"""

	input:
		config_in = "{population}/config.ini"

	output:
		out = directory("{population}/out")		

	conda: "camisim_env.yaml"
	
	shell:
		"""
			rm -rf {wildcards.population}/out/
			python metagenomesimulation.py {input.config_in}
		"""

rule population_input_files:
	"""
		Comment here
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
