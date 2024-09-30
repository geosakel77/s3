import csv
from fileinput import close
from symtable import Class
from typing import List, Dict, Any

from numpy.ma.extras import unique
from numpy.random import PCG64, SeedSequence
from treelib import Node, Tree
from netaddr.ip.iana import query
from pycti import OpenCTIApiClient
from datasketch import MinHash
from pyexpat.errors import messages
from regex import search
from openai import OpenAI, api_key
import json, os, csv, json
from owlready2 import *
from rdflib import Graph, Namespace
from rdflib.plugins.sparql import prepareQuery
import pandas as pd
import xml.etree.ElementTree as ET


class Client:
    def __init__(self, config):
        self.config = config


class OpenCTIClient(Client):
    def __init__(self, config, api_url='api_url', api_key='api_key'):
        super().__init__(config)
        self.api_url = self.config[api_url]
        self.api_key = self.config[api_key]
        self.open_cti_client = OpenCTIApiClient(self.api_url, self.api_key)

    def get_malware(self, search_term="windows"):
        return self.open_cti_client.malware.list(search=search_term)


class OpenAIClient(Client):
    def __init__(self, config):
        super().__init__(config)
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
        return self.client.chat.completions.create(messages=messages_list, model=self.config['openai_model'],
                                                   temperature=0).choices[
            0].message.content


class OntologyClient(Client):
    def __init__(self, config, path_key, path_entry_key):
        super().__init__(config)
        self.path_key = path_key
        self.path_entry_key = path_entry_key
        self.extracted_data = None
        self.graph = Graph()
        self.graph.parse(self.config[self.path_entry_key], format="xml")
        print("Finish Initialization")


class JSONClient(Client):

    def __init__(self, config, path_key):
        super().__init__(config)
        self.path_key = path_key
        self.data = self._load_data()

    def _load_data(self):
        print("Load Data")

        with open(self.config[self.path_key], 'r') as f:
            data = json.load(f)

        return data


class OntologyNACEClient(OntologyClient):
    def __init__(self, config, path_key='nace_path', path_entry_key='nace_entry'):
        super().__init__(config, path_key, path_entry_key)
        self.loadeddata = JSONClient(config, path_key='nace_json')

    def write_to_file(self, filepath):
        print(f"Writing extracted data to: {filepath}")
        with open(filepath, "w") as f:
            f.write(json.dumps(self.extracted_data))

    def get_data(self):
        extracted_data = {}
        print("Extracting Top Concepts")
        top_concepts = self._get_top_concept()
        print(f"{len(top_concepts)} Top Concepts Extracted")
        for concept in top_concepts:
            print(f"Extracting first level of narrower concepts for: {concept}")
            concept_dic = self._get_data_from_named_individual(concept)
            narrower_concepts = self._get_narrower_concept(concept)
            narrower_concepts_data = []
            concept_dic["narrower_concepts"] = narrower_concepts
            if len(narrower_concepts) > 0:
                print(f"{len(narrower_concepts)} narrower concepts of first level extracted")
                for narrower_concept in narrower_concepts:
                    print(f"Extracting second level of narrower concepts for: {narrower_concept}")
                    second_level_narrower_concepts = self._get_narrower_concept(narrower_concept)
                    first_level_narrower_concept_dic = self._get_data_from_named_individual(narrower_concept)
                    first_level_narrower_concepts_data = []
                    first_level_narrower_concept_dic[narrower_concept] = second_level_narrower_concepts
                    if len(second_level_narrower_concepts) > 0:
                        print(f"{len(second_level_narrower_concepts)} narrower concepts of second level extracted")
                        for second_level_narrower_concept in second_level_narrower_concepts:
                            print(f"Extracting third level of narrower concepts for: {second_level_narrower_concept}")
                            third_level_narrower_concepts = self._get_narrower_concept(second_level_narrower_concept)
                            second_level_narrower_concept_dic = self._get_data_from_named_individual(
                                second_level_narrower_concept)
                            second_level_narrower_concepts_data = []
                            second_level_narrower_concept_dic[
                                second_level_narrower_concept] = third_level_narrower_concepts
                            if len(third_level_narrower_concepts) > 0:
                                print(
                                    f"{len(third_level_narrower_concepts)} narrower concepts of third level extracted")
                                for third_level_narrower_concept in third_level_narrower_concepts:
                                    print(
                                        f"Extracting fourth level of narrower concepts for: {third_level_narrower_concept}")
                                    fourth_level_narrower_concepts = self._get_narrower_concept(
                                        third_level_narrower_concept)
                                    third_level_narrower_concept_dic = self._get_data_from_named_individual(
                                        third_level_narrower_concept)
                                    third_level_narrower_concepts_data = []
                                    third_level_narrower_concept_dic[
                                        third_level_narrower_concept] = fourth_level_narrower_concepts
                                    if len(fourth_level_narrower_concepts) > 0:
                                        print(
                                            f"{len(fourth_level_narrower_concepts)} narrower concepts of fourth level extracted")
                                        for fourth_level_narrower_concept in fourth_level_narrower_concepts:
                                            fourth_level_narrower_concept_dic = self._get_data_from_named_individual(
                                                fourth_level_narrower_concept)
                                            third_level_narrower_concepts_data.append(
                                                {fourth_level_narrower_concept: fourth_level_narrower_concept_dic})
                                    third_level_narrower_concept_dic[
                                        "third_level_narrower_concepts_data"] = third_level_narrower_concepts_data
                                    second_level_narrower_concepts_data.append(
                                        {third_level_narrower_concept: third_level_narrower_concept_dic})
                            second_level_narrower_concept_dic[
                                "second_level_narrower_concepts_data"] = second_level_narrower_concepts_data
                            first_level_narrower_concepts_data.append(
                                {second_level_narrower_concept: second_level_narrower_concept_dic})
                    first_level_narrower_concept_dic[
                        "first_level_narrower_concepts_data"] = first_level_narrower_concepts_data
                    narrower_concepts_data.append({narrower_concept: first_level_narrower_concept_dic})

            concept_dic["narrower_concepts_data"] = narrower_concepts_data
            extracted_data[concept] = concept_dic
        print(extracted_data)
        self.extracted_data = extracted_data
        return extracted_data

    def _get_top_concept(self):
        sparql_query = """
        SELECT ?y ?x 
        WHERE {  
                 ?y rdf:type skos:ConceptScheme . 
                 ?y skos:hasTopConcept ?x .
                 }"""
        query_result = self.graph.query(sparql_query)
        return [row.x for row in query_result]

    def _get_narrower_concept(self, broader):
        sparql_query = prepareQuery("SELECT ?x WHERE {?broader skos:narrower ?x}")
        query_result = self.graph.query(sparql_query, initBindings={'broader': broader})
        print(f"Query Result: {len(query_result)}")
        return [row.x for row in query_result]

    def _get_data_from_named_individual(self, name):
        XKOS = Namespace("http://rdf-vocabulary.ddialliance.org/xkos#")
        DCT = Namespace("http://purl.org/dc/terms/")
        sparql_query = prepareQuery(
            "SELECT ?identifier ?notation ?prefLabel ?definition ?coreContentNote ?additionalContentNote ?exclusionNote WHERE { ?name dct:identifier ?identifier . ?name skos:notation ?notation . ?name skos:prefLabel ?prefLabel . ?name skos:definition ?definition . ?name xkos:coreContentNote ?coreContentNote . ?name xkos:additionalContentNote ?additionalContentNote . ?name xkos:exclusionNote ?exclusionNote . }",
            initNs={"xkos": XKOS, "dct": DCT})
        query_result = self.graph.query(sparql_query, initBindings={'name': name})
        print(len(query_result))
        exported_data = {}
        if len(query_result) == 1:
            for row in query_result:
                exported_data = {'identifier': row.identifier.value,
                                 'notation': row.notation.value,
                                 "prefLabel": row.prefLabel.value,
                                 "definition": row.definition.value,
                                 "coreContentNote": row.coreContentNote.value,
                                 "additionalContentNote": row.additionalContentNote.value,
                                 "exclusionNote": row.exclusionNote.value
                                 }
        else:
            sparql_query = prepareQuery(
                "SELECT ?identifier ?notation ?prefLabel ?definition ?coreContentNote ?additionalContentNote  WHERE { ?name dct:identifier ?identifier . ?name skos:notation ?notation . ?name skos:prefLabel ?prefLabel . ?name skos:definition ?definition . ?name xkos:coreContentNote ?coreContentNote . ?name xkos:additionalContentNote ?additionalContentNote . }",
                initNs={"xkos": XKOS, "dct": DCT})
            query_result = self.graph.query(sparql_query, initBindings={'name': name})
            print(len(query_result))
            if len(query_result) == 1:
                for row in query_result:
                    exported_data = {'identifier': row.identifier.value,
                                     'notation': row.notation.value,
                                     "prefLabel": row.prefLabel.value,
                                     "definition": row.definition.value,
                                     "coreContentNote": row.coreContentNote.value,
                                     "additionalContentNote": row.additionalContentNote.value
                                     }
            else:
                sparql_query = prepareQuery(
                    "SELECT ?identifier ?notation ?prefLabel ?definition ?coreContentNote ?exclusionNote  WHERE { ?name dct:identifier ?identifier . ?name skos:notation ?notation . ?name skos:prefLabel ?prefLabel . ?name skos:definition ?definition . ?name xkos:coreContentNote ?coreContentNote . ?name xkos:exclusionNote ?exclusionNote . }",
                    initNs={"xkos": XKOS, "dct": DCT})
                query_result = self.graph.query(sparql_query, initBindings={'name': name})
                print(len(query_result))
                if len(query_result) == 1:
                    for row in query_result:
                        exported_data = {'identifier': row.identifier.value,
                                         'notation': row.notation.value,
                                         "prefLabel": row.prefLabel.value,
                                         "definition": row.definition.value,
                                         "coreContentNote": row.coreContentNote.value,
                                         "exclusionNote": row.exclusionNote.value
                                         }
                else:
                    sparql_query = prepareQuery(
                        "SELECT ?identifier ?notation ?prefLabel ?definition ?coreContentNote WHERE { ?name dct:identifier ?identifier . ?name skos:notation ?notation . ?name skos:prefLabel ?prefLabel . ?name skos:definition ?definition . ?name xkos:coreContentNote ?coreContentNote . }",
                        initNs={"xkos": XKOS, "dct": DCT})
                    query_result = self.graph.query(sparql_query, initBindings={'name': name})
                    print(len(query_result))
                    if len(query_result) == 1:
                        for row in query_result:
                            exported_data = {'identifier': row.identifier.value,
                                             'notation': row.notation.value,
                                             "prefLabel": row.prefLabel.value,
                                             "definition": row.definition.value,
                                             "coreContentNote": row.coreContentNote.value,
                                             }
        return exported_data


class OntologyFIBOClient(OntologyClient):
    def __init__(self, config, path_key='fibo_path', path_entry_key='fibo_entry'):
        super().__init__(config, path_key, path_entry_key)
        self.file_system_tree = self._walk_files()

    def _walk_files(self):
        tree = Tree()
        rootname = 'fibodata'
        os.walk(self.config[self.path_key])
        dataroots = []
        datadirs = {}
        datafiles = {}
        for root, dirs, files in os.walk(self.config[self.path_key]):
            dataroots.append(root)
            datadirs[root] = dirs
            datafiles[root] = files
        print(f"Create Node : {dataroots[0]}")
        tree.create_node(rootname, dataroots[0], data=dataroots[0])
        for root in dataroots:
            directories = datadirs[root]
            for directory in directories:
                identifier = "".join((root, "\\", directory))
                data = "".join((root, "\\", directory))
                print(f"Create Node : {directory} -- with identifier {identifier} -- with data {data}")
                tree.create_node(tag=directory, identifier=identifier, parent=root, data=data)

            files = datafiles[root]
            for file in files:
                identifier = "".join((root, "\\", file))
                data = "".join((root, "\\", file))
                print(f"Create Node : {file} -- with identifier {identifier} -- with data {data}")
                tree.create_node(tag=file, identifier=identifier, parent=root, data=data)

        tree.save2file("testdata.txt")
        return tree


class OntologyGPOClient(OntologyClient):
    def __init__(self, config, path_key='gpo_path', path_entry_key='gpo_entry'):
        super().__init__(config, path_key, path_entry_key)
        self.get_data()

    def get_data(self):
        labels = self._get_labels()
        properties_labels = self._get_properties_labels()
        class_properties_constraints = self._get_class_constraints()
        ontology_data = self._ontology_classes_factory(labels, properties_labels, class_properties_constraints)
        self.extracted_data = ontology_data
        return ontology_data

    def _get_labels(self):
        sparql_query = """
                    SELECT ?y ?x 
                    WHERE {  
                             ?y skos:prefLabel ?x .
                             }"""
        query_result = self.graph.query(sparql_query)
        return [(row.y, row.x) for row in query_result]

    def _get_properties_labels(self):
        sparql_query = """
                            SELECT ?y ?x 
                            WHERE {  
                                     ?y rdf:type owl:ObjectProperty .
                                     ?y skos:prefLabel ?x .
                                     }"""
        query_result = self.graph.query(sparql_query)
        return [(row.y, row.x) for row in query_result]

    def _get_class_constraints(self):
        sparql_query = """
                                    SELECT ?y ?k ?x ?t ?z
                                    WHERE {  
                                             ?y rdf:type owl:Class .
                                             ?k owl:onProperty ?x .
                                             ?k owl:someValuesFrom ?z

                                             }"""
        query_result = self.graph.query(sparql_query)
        return [(row.y, row.x, row.z) for row in query_result]

    def _ontology_classes_factory(self, labels, properties_labels, class_properties_constraints):
        labels_dict = {}
        properties_labels_dict = {}
        for label in labels:
            labels_dict[label[0]] = label[1].value
        for property in properties_labels:
            properties_labels_dict[property[0]] = property[1].value

        ontology_data = {}
        for constraint in class_properties_constraints:
            if constraint[0] in labels_dict.keys():
                if constraint[1] in properties_labels_dict.keys():
                    if constraint[2] in labels_dict.keys():
                        if not labels_dict[constraint[0]] in ontology_data.keys():
                            temp = self.OntologyClass(labels_dict[constraint[0]])
                            temp.properties_labels.append(properties_labels_dict[constraint[1]])
                            temp.constraints[properties_labels_dict[constraint[1]]] = [labels_dict[constraint[2]]]
                            ontology_data[labels_dict[constraint[0]]] = temp
                        else:
                            temp = ontology_data[labels_dict[constraint[0]]]
                            temp.properties_labels.append(properties_labels_dict[constraint[1]])
                            temp.constraints[properties_labels_dict[constraint[1]]] = [labels_dict[constraint[2]]]
                            ontology_data[labels_dict[constraint[0]]] = temp

        for key in ontology_data.keys():
            ontology_data[key].unique_values()
        return ontology_data

    class OntologyClass:
        def __init__(self, label):
            self.label = label
            self.properties_labels = []
            self.constraints = {}

        def unique_values(self):
            self.properties_labels = list(set(self.properties_labels))

        def to_tuple(self):
            return self.label, self.properties_labels, self.constraints


class CSVClient(Client):

    def __init__(self, config, path_key):
        super().__init__(config)
        self.path_key = path_key
        self.data = self._load_data()

    def _load_data(self):
        print("Load Data")
        data = pd.read_csv(self.config[self.path_key], encoding='utf-8', dtype=str)
        return data


class CompaniesClient(CSVClient):
    def __init__(self, config, path_key='companies_path'):
        super().__init__(config, path_key)
        self.data_keys = self.data.keys()

    def get_company(self, index):
        print(self.data.keys())
        return self.data[index:index + 1]

    def get_companies_sample(self, size, seed=0):
        ss = SeedSequence(seed)
        state = PCG64(ss)
        return self.data.sample(n=size, random_state=state)


class XMLClient(Client):
    def __init__(self, config, path_key):
        super().__init__(config)
        self.path_key = path_key
        self.tree = ET.parse(self.config[self.path_key])


class CPEClient(XMLClient):
    def __init__(self, config, path_key="cpe_path"):
        super().__init__(config, path_key)
