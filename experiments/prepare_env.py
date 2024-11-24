from experiments.experiments_relevance_metric.prepare_relevance_metric_env import prepare_relevance_metric_env
from experiments.experiments_actionability_metric.prepare_actionability_metric_env import prepare_actionability_metric_env
from config.config import read_config

def run():
    print(f"Starting the  experimental environment preparation...")
    config = read_config(filepath="../config/config.ini")
    #prepare_relevance_metric_env(config)
    prepare_actionability_metric_env(config)
    print(f"Experimental environment preparation complete.")

if __name__ == '__main__':
    run()