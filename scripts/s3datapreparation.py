from s3lib.s3clientslib import OntologyNACEClient,OntologyPTOClient

def data_rel_preparation(config):
    """
    Prepares and writes NACE and PTO data using the specified configuration.

    This function performs the following steps:
    1. Initializes NACE and PTO clients with the provided configuration.
    2. Fetches NACE data and writes it to a file.
    3. Fetches PTO data and writes it to a file.

    Parameters:
    config (dict): Configuration settings required by NACE and PTO clients.

    Returns:
    None
    """
    print("Starting Data Preparation...")
    print("Preparing NACE Data...")
    nace_client = OntologyNACEClient(config)
    nace_client.get_data()
    nace_client.write_to_file()
    print("Data Preparation Complete")
    print("Preparing PTO Data...")
    pto_client = OntologyPTOClient(config)
    pto_client.get_data()
    pto_client.write_to_file()
    print("Data Preparation Complete")

def data_act_preparation(config):
    #TODO
    pass