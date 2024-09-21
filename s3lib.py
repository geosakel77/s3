from typing import List, Dict, Any

from netaddr.ip.iana import query
from pycti import OpenCTIApiClient
from datasketch import MinHash
from pyexpat.errors import messages
from regex import search
from openai import OpenAI

from config import read_config
from owlready2 import *
from rdflib import Graph,Namespace
from rdflib.plugins.sparql import prepareQuery

class OpenCTIClient:
    def __init__(self, api_url, api_key):
        self.api_url = api_url
        self.api_key = api_key
        self.open_cti_client = OpenCTIApiClient(self.api_url, self.api_key)

    def get_malware(self, search_term="windows"):
        return self.open_cti_client.malware.list(search=search_term)


class OpenAIClient:
    def __init__(self,config):
        self.config = config
        self.client = OpenAI(api_key=self.config['openai_api_key'], organization=self.config['openai_organization_id'],
                             project=self.config['openai_project_id'])

    def call_openai(self, message):

        messages_list: list[dict[str, str | Any]] = [{
            "role": "user",
            "content": message
        }]
        response = self._call_run(messages_list)
        return response

    def _call_run(self, messages_list):
        return self.client.chat.completions.create(messages=messages_list, model=self.config['openai_model'],temperature=0).choices[
            0].message.content

class OntologyClient:
    def __init__(self,config,path_key,path_entry_key):
        self.path_key=path_key
        self.path_entry_key=path_entry_key
        self.config = config
        self.graph = Graph()
        self.graph.parse(self.config[self.path_entry_key], format="xml")
        print("Finish Initialization")



class OntologyFIBOClient(OntologyClient):
    def __init__(self,config,path_key='fibo_path',path_entry_key='fibo_entry'):
        super().__init__(config,path_key,path_entry_key)

class OntologyNACEClient(OntologyClient):
    def __init__(self, config, path_key='nace_path', path_entry_key='nace_entry'):
        super().__init__(config, path_key, path_entry_key)


    def get_data(self):

        topconcepts = self._get_top_concept()
        testdata = self._get_narrower_concept(topconcepts[0])
        testdata1 = self._get_data_from_named_individual(topconcepts[0])
        print(testdata)
        print(testdata1)

    def _get_top_concept(self):
        sparql_query = """
        SELECT ?y ?x 
        WHERE {  
                 ?y rdf:type skos:ConceptScheme . 
                 ?y skos:hasTopConcept ?x .
                 }"""
        query_result = self.graph.query(sparql_query)
        return [row.x for row in query_result]

    def _get_narrower_concept(self,broader):
        sparql_query = prepareQuery("SELECT ?x WHERE {?broader skos:narrower ?x}")
        query_result = self.graph.query(sparql_query,initBindings={'broader':broader})
        print(len(query_result))
        return [row.x for row in query_result]

    def _get_data_from_named_individual(self, name):
        XKOS = Namespace("http://rdf-vocabulary.ddialliance.org/xkos#")
        sparql_query = prepareQuery("SELECT ?identifier ?prefLabel ?definition ?coreContentNote WHERE { ?name skos:notation ?identifier . ?name skos:prefLabel ?prefLabel . ?name skos:definition ?definition . ?name xkos:coreContentNote ?coreContentNote . }",initNs={"xkos":XKOS})

        query_result = self.graph.query(sparql_query,initBindings={'name':name})
        #query_result = self.graph.query(sparql_query1,initNs={"xkos":XKOS})

        print(len(query_result))

        if len(query_result) == 1:
            for row in query_result:
               exported_data={'identifier':row.identifier,
                              "prefLabel":row.prefLabel,
                              "definition":row.definition,
                              "coreContentNote":row.coreContentNote
                              }
        else:
            exported_data={}
        return exported_data




