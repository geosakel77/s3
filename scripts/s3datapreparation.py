from config import read_config
from s3lib import OntologyNACEClient
from owlready2 import *
from rdflib import Graph
import pprint

def run():
    CONFIG = read_config("../config.ini")
    #client= OntologyNACEClient(CONFIG)
    #for cls in client.ontology.classes():
    clientNACE= OntologyNACEClient(CONFIG)
    clientNACE.get_data()




if __name__ == '__main__':
    run()