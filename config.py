import configparser

import configparser

from stix2validator.v21.musts import process


def read_config(filepath="config.ini"):
	# Create a ConfigParser object
	config = configparser.ConfigParser()

	# Read the configuration file
	config.read(filepath)

	# Access values from the configuration file
	debug_mode = config.getboolean('general', 'debug')
	log_level = config.get('general', 'log_level')
	api_url = config.get('opencti', 'api_url')
	api_key = config.get('opencti', 'api_key')
	openai_api_key = config.get('openai', 'openai_api_key')
	openai_organization_id = config.get('openai', 'organization_id')
	openai_project_id = config.get('openai', 'project_id')
	openai_model= config.get('openai', 'model')
	fibo_path= config.get('ontology', 'fibo_path')
	fibo_entry= config.get('ontology', 'fibo_entry')
	dit_path= config.get('ontology', 'dit_path')
	dit_entry= config.get('ontology', 'dit_entry')
	nace_path= config.get('ontology', 'nace_path')
	nace_entry= config.get('ontology', 'nace_entry')
	skos_entry= config.get('ontology', 'skos_entry')
	dcat_entry= config.get('ontology', 'dcat_entry')
	nace_json = config.get('ontology', 'nace_json')
	gpo_path= config.get('ontology', 'gpo_path')
	gpo_entry= config.get('ontology', 'gpo_entry')
	companies_entry= config.get('dataset', 'companies_path')
	cpe_path= config.get('dataset', 'cpe_path')
	# Return a dictionary with the retrieved values
	config_values = {
		'debug_mode': debug_mode,
		'log_level': log_level,
		'api_url': api_url,
		'api_key': api_key,
		'openai_api_key': openai_api_key,
		'openai_organization_id': openai_organization_id,
		'openai_project_id': openai_project_id,
		'openai_model': openai_model,
		'fibo_path': fibo_path,
		'fibo_entry': fibo_entry,
		'dit_path': dit_path,
		'dit_entry': dit_entry,
		'nace_path': nace_path,
		'nace_entry': nace_entry,
		'skos_entry': skos_entry,
		'dcat_entry': dcat_entry,
		'nace_json': nace_json,
		'companies_path': companies_entry,
		'gpo_path': gpo_path,
		'gpo_entry': gpo_entry,
		'cpe_path': cpe_path
	}

	return config_values

