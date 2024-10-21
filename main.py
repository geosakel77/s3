from http.client import responses

from stix2validator.v21.musts import process

from config.config import read_config
from scripts.s3datapreparation import data_preparation
from scripts.s3prepareorganizations import prepare_organizations


def run():
    CONFIG = read_config('config/config.ini')

    print("Preparing organizations configuration files...")
    prepare_organizations(CONFIG)
    print("Organizations' configuration has been prepared has been ")





# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    run()
