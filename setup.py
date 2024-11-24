from config.config import read_config
from scripts.s3datapreparation import data_rel_preparation,data_act_preparation
from scripts.s3prepareorganizations import prepare_rel_organizations, prepare_act_organizations


def run_relevance_metric_setup():
    config = read_config('config/config.ini')
    print("Preparing relevance organizations configuration files...")
    prepare_rel_organizations(config)
    print("Organizations' configuration has been prepared.")
    print("Preparing datasets...")
    data_rel_preparation(config)
    print("Datasets has been prepared.")

def run_actionability_metric_setup():
    config = read_config('config/config.ini')
    print("Preparing actionability organizations configuration files...")
    prepare_act_organizations(config)
    print("Organizations' configuration has been prepared.")
    print("Preparing datasets...")
    data_act_preparation(config)
    print("Datasets has been prepared.")


if __name__ == '__main__':
    run_relevance_metric_setup()
    run_actionability_metric_setup()