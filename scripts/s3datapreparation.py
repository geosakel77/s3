from rich.jupyter import display

from config.config import read_config
from s3lib.libclients import OntologyNACEClient, OntologyFIBOClient, OntologyGPOClient, CPEClient, OntologyECCFClient, \
    OntologyPTOClient, CompaniesClient
from owlready2 import *
from rdflib import Graph
import pprint

def data_preparation():
    CONFIG = read_config("../config/config.ini")
    #Data Preparation Script
    print("Starting Data Preparation and Testing Script...")
    print("Testing Companies Dataset")
    companies_client=CompaniesClient(CONFIG)
    print(companies_client.data_keys)
    indust =companies_client.get_industries()
    print(indust)
    print(len(indust))

    #sample= companies_client.get_companies_sample(5,industry='capital markets')

    #print(sample.to_string())


    #clientNACE= OntologyNACEClient(CONFIG)
    #clientNACE.get_data()
    #clientNACE.write_to_file(CONFIG['nace_json'])
    #clientNACE.get_data()
    #clientFIBO = OntologyFIBOClient(CONFIG)
    #clientPTO =OntologyPTOClient(CONFIG)
    #print(clientPTO.loadeddata.data)
    #clientPTO.write_to_file(CONFIG['pto_json'])
    #clientGPO = OntologyGPOClient(CONFIG)
    #for key in clientGPO.extracted_data.keys():
    #    print(clientGPO.extracted_data[key].to_tuple())
    #clientCPE = CPEClient(CONFIG)
    #clientCPE.extracted_data[0].to_print()
    #clientECCF = OntologyECCFClient(CONFIG)
    #for key in clientECCF.extracted_data.keys():
    #    print(clientECCF.extracted_data[key].to_tuple())
    print("Testing Companies Dataset")
