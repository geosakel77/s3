from config.config import read_config
from scripts.s3datapreparation import data_preparation
from scripts.s3prepareorganizations import prepare_organizations

def run():
    CONFIG = read_config('config/config.ini')
    print("Preparing organizations configuration files...")
    prepare_organizations(CONFIG)
    print("Organizations' configuration has been prepared.")
    print("Preparing datasets...")
    data_preparation(CONFIG)
    print("Datasets has been prepared.")

if __name__ == '__main__':
    run()
