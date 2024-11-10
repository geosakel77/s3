from config.config import read_config
from s3lib.s3clientslib import OntologyNACEClient,OntologyPTOClient

def data_preparation(CONFIG):
    print("Starting Data Preparation...")
    print("Preparing NACE Data...")
    nace_client = OntologyNACEClient(CONFIG)
    nace_client.get_data()
    nace_client.write_to_file()
    print("Data Preparation Complete")
    print("Preparing PTO Data...")
    pto_client = OntologyPTOClient(CONFIG)
    pto_client.get_data()
    pto_client.write_to_file()
    print("Data Preparation Complete")
