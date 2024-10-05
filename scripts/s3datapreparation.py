from config import read_config
from s3lib import OntologyNACEClient, OntologyFIBOClient, OntologyGPOClient, CPEClient, OntologyECCFClient, \
    OntologyPTOClient
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
    clientPTO =OntologyPTOClient(CONFIG)
    print(clientPTO.loadeddata.data)
    #clientPTO.write_to_file(CONFIG['pto_json'])
    #clientGPO = OntologyGPOClient(CONFIG)
    #for key in clientGPO.extracted_data.keys():
    #    print(clientGPO.extracted_data[key].to_tuple())
    #clientCPE = CPEClient(CONFIG)
    #clientCPE.extracted_data[0].to_print()
    #clientECCF = OntologyECCFClient(CONFIG)
    #for key in clientECCF.extracted_data.keys():
    #    print(clientECCF.extracted_data[key].to_tuple())




if __name__ == '__main__':
    run()