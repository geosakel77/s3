import json
from experiments.experiments_relevance_metric.prepare_relevance_metric_env import prepare_relevance_metric_env
from experiments.experiments_actionability_metric.prepare_actionability_metric_env import prepare_actionability_metric_env
from config.config import read_config
from s3lib.s3clientslib import LocalCTIClient


def prepare_cti_data(config):
    print("Preparing CTI data.")
    cti_client = LocalCTIClient(config)

def prepare_validation_data(config):
    print("Preparing validation data...")
    path = config['validation_dataset']
    number = config['validation_data_number']

    #open_cti_client = OpenCTIClient(config)
    #for i in range(int(number)):
    #    #TODO
    #    data=""
    #    data=open_cti_client.get_malware()
    #    filepath = f"{path}\\{i}.json"
    #    with open(filepath, 'w') as f:
    #        json_object = json.dumps(data, indent=4)
    #        f.write(json_object)
    #    break


def run():
    print(f"Starting the  experimental environment preparation...")
    config = read_config(filepath="../config/config.ini")
    #prepare_relevance_metric_env(config)
    prepare_cti_data(config)
    #prepare_validation_data(config)
    #prepare_actionability_metric_env(config)
    print(f"Experimental environment preparation complete.")

if __name__ == '__main__':
    run()