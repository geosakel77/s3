from config import read_config
from s3lib import OntologyNACEClient,OntologyFIBOClient, OntologyGPOClient
from owlready2 import *
from rdflib import Graph
import pprint

def run():
    CONFIG = read_config("../config.ini")
    #Data Preparation Script
    #clientNACE= OntologyNACEClient(CONFIG)
    #clientNACE.get_data()
    #clientNACE.write_to_file(CONFIG['nace_json'])
    #clientNACE.get_data()
    #clientFIBO = OntologyFIBOClient(CONFIG)
    #clientGPO = OntologyGPOClient(CONFIG)
    #clientGPO.get_data()





if __name__ == '__main__':
    run()