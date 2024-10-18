
from typing import  Any
from urllib.error import URLError

from numpy.random import PCG64, SeedSequence
from pycti import OpenCTIApiClient
from openai import OpenAI
import json
from owlready2 import *
from rdflib import Graph, Namespace, URIRef
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


class OntologyGPOClient(OntologyClient):
    def __init__(self, config, path_key='gpo_path', path_entry_key='gpo_entry'):
        super().__init__(config, path_key, path_entry_key)
        self.get_data()

    def get_data(self):
        labels = self._get_labels()
        properties_labels = self._get_properties_labels()
        class_properties_constraints = self._get_class_constraints()
        subclasses=self._get_subclasses()
        ontology_data = self._ontology_classes_factory(labels, properties_labels, class_properties_constraints,subclasses)
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

    def _get_subclasses(self):
        sparql_query = """
                    SELECT ?y ?x 
                    WHERE {  ?y rdf:type owl:Class .
                             ?y rdfs:subClassOf ?x .
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

    def _ontology_classes_factory(self, labels, properties_labels, class_properties_constraints,subclasses):
        labels_dict = {}
        properties_labels_dict = {}
        subclasses_dict = {}
        for label in labels:
            labels_dict[label[0]] = label[1].value
        for property in properties_labels:
            properties_labels_dict[property[0]] = property[1].value
        for subclass in subclasses:
            uri = URIRef(subclass[1])
            if uri in labels_dict.keys() and subclass[0] in labels_dict.keys():
                if subclass[0] in subclasses_dict.keys():
                    subclasses_dict[labels_dict[subclass[0]]].append(labels_dict[uri])
                else:
                    subclasses_dict[labels_dict[subclass[0]]] = [labels_dict[uri]]
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
            if key in subclasses_dict.keys():
                ontology_data[key].subclasses = subclasses_dict[key]
            ontology_data[key].unique_values()
        return ontology_data

    class OntologyClass:
        def __init__(self, label):
            self.label = label
            self.properties_labels = []
            self.constraints = {}
            self.subclasses = {}

        def unique_values(self):
            self.properties_labels = list(set(self.properties_labels))

        def to_tuple(self):
            return self.label, self.properties_labels, self.constraints, self.subclasses


class OntologyECCFClient(OntologyGPOClient):
    def __init__(self, config, path_key='eccf_path', path_entry_key='eccf_entry'):
        super().__init__(config,path_key,path_entry_key)

    def _get_labels(self):
        sparql_query = """
                    SELECT ?y ?x 
                    WHERE {  
                             ?y rdf:type owl:Class . 
                             ?y rdfs:label ?x .
                             }"""
        query_result = self.graph.query(sparql_query)
        return [(row.y, row.x) for row in query_result]

    def _get_properties_labels(self):
        sparql_query = """
                            SELECT ?y ?x 
                            WHERE {  
                                     ?y rdf:type owl:ObjectProperty .
                                     ?y rdfs:label ?x .
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
        return self.data[index:index + 1]

    def get_companies_sample(self, size,industry="", seed=0):
        ss = SeedSequence(seed)
        state = PCG64(ss)
        if len(industry)>1:
            returned_sample = self.data.loc[self.data['industry'].isin([industry])].sample(n=size,random_state=state)
        else:
            returned_sample=self.data.sample(n=size, random_state=state)

        return returned_sample

    def get_industries(self):
        result= list(set(self.data['industry'].values.tolist()))
        for r in result:
            if type(r)==float:
                result.pop(result.index(r))
        result.sort()
        return result

class XMLClient(Client):
    def __init__(self, config, path_key):
        super().__init__(config)
        self.path_key = path_key
        self.tree = ET.parse(self.config[self.path_key])
        self.extracted_data = None


class CPEClient(XMLClient):
    def __init__(self, config, path_key="cpe_path"):
        super().__init__(config, path_key)
        self._get_data()

    def _get_data(self):
        data = []
        root = self.tree.getroot()
        for child in root:
            if 'cpe-item' in child.tag:
                name = child.attrib['name']
                title = None
                references = None
                cpe23 = None
                for child1 in child:
                    if "title" in child1.tag:
                        title = child1.text
                    elif "references" in child1.tag:
                        references = []
                        for child2 in child1:
                            references.append((child2.attrib['href'], child2.text))
                    elif "cpe23-item" in child1.tag:
                        cpe23 = child1.attrib['name']
                data.append(self.CPEItem(name, title, references, cpe23))
        self.extracted_data = data

    class CPEItem:
        def __init__(self, name, title, references, cpe23):
            self.name = name
            self.title = title
            self.references = references
            self.cpe23 = self._cpe23_analysis(cpe23)

        def _cpe23_analysis(self, cpe23):
            data = cpe23.split(':')
            values = {}
            if data[2] == 'a':
                values['part'] = "application"
            elif data[2] == 'o':
                values['part'] = "operating system"
            elif data[2] == 'h':
                values['part'] = "hardware"
            else:
                values['part'] = ''

            if data[3] != '*':
                values['vendor'] = data[3]
            else:
                values['vendor'] = None

            if data[4] != '*':
                values['product'] = data[4]
            else:
                values['product'] = None

            if data[5] != '*':
                values['version'] = data[5]
            else:
                values['version'] = None

            if data[6] != '*':
                values['update'] = data[6]
            else:
                values['update'] = None

            if data[7] != '*':
                values['edition'] = data[7]
            else:
                values['edition'] = None

            if data[8] != '*':
                values['language'] = data[8]
            else:
                values['language'] = None

            if data[9] != '*':
                values['sw_edition'] = data[9]
            else:
                values['sw_edition'] = None

            if data[10] != '*':
                values['target_sw'] = data[10]
            else:
                values['target_sw'] = None

            if data[11] != '*':
                values['target_hw'] = data[11]
            else:
                values['target_hw'] = None

            if data[12] != '*':
                values['other'] = data[12]
            else:
                values['other'] = None
            return values

        def to_print(self):
            print(self.name)
            print(self.title)
            print(self.references)
            print(self.cpe23)


class OntologyPTOClient(OntologyClient):
    def __init__(self, config, path_key='pto_path',path_entry_key="pto_entry"):
        super().__init__(config, path_key,path_entry_key)
        self.loadeddata = JSONClient(config, path_key='pto_json')


    def write_to_file(self, filepath):
        print(f"Writing extracted data to: {filepath}")
        with open(filepath, "w") as f:
            f.write(json.dumps(self.extracted_data))

    def get_data(self):
        labels = self._get_labels()
        sources = self._get_sources()
        subclasses = self._get_subclasses()
        ontology_data = self._ontology_classes_factory(labels, sources, subclasses)
        for key in ontology_data.keys():
            ontology_data[key].update_data()
            ontology_data[key]=ontology_data[key].to_tuple()
        self.extracted_data = ontology_data
        return ontology_data

    def _get_labels(self):
        sparql_query = """
                    SELECT ?y ?x 
                    WHERE {  
                             ?y rdf:type owl:Class . 
                             ?y rdfs:label ?x .
                             }"""
        query_result = self.graph.query(sparql_query)
        return [(row.y, row.x) for row in query_result]

    def _get_sources(self):
        sparql_query = """
                            SELECT ?y ?x 
                            WHERE {  
                                     ?y rdf:type owl:Class . 
                                     ?y wdrs:describedby ?x .
                                     }"""
        query_result = self.graph.query(sparql_query)
        return [(row.y, row.x) for row in query_result]

    def _get_subclasses(self):
        sparql_query = """
                    SELECT ?y ?x 
                    WHERE {  ?y rdf:type owl:Class .
                             ?y rdfs:subClassOf ?x .
                             }"""
        query_result = self.graph.query(sparql_query)
        return [(row.y, row.x) for row in query_result]

    def _ontology_classes_factory(self, labels, sources,subclasses):
        labels_dict = {}
        sources_dict = {}
        subclasses_dict = {}
        for label in labels:
            labels_dict[label[0]] = label[1].value
        for source in sources:
            if "rdf" in source[1].n3():
                sources_dict[source[0]] = source[1]
        for subclass in subclasses:
            uri = URIRef(subclass[1])
            if uri in labels_dict.keys() and subclass[0] in labels_dict.keys():
                if subclass[0] in subclasses_dict.keys():
                    subclasses_dict[labels_dict[subclass[0]]].append(labels_dict[uri])
                else:
                    subclasses_dict[labels_dict[subclass[0]]] = [labels_dict[uri]]
        ontology_data = {}
        for key in labels_dict.keys():
            if not labels_dict[key] in ontology_data.keys():
                temp = self.OntologyClass(labels_dict[key])
                temp.source.append(sources_dict[key])
                ontology_data[labels_dict[key]] = temp
            else:
                temp = ontology_data[labels_dict[key]]
                temp.source.append(sources_dict[key])
                ontology_data[labels_dict[key]] = temp
        for key in ontology_data.keys():
            if key in subclasses_dict.keys():
                ontology_data[key].subclasses = subclasses_dict[key]
        return ontology_data

    class OntologyClass:
        def __init__(self, label):
            self.label = label
            self.source = []
            self.subclasses = {}
            self.comments=[]

        def update_data(self):
            comments=[]
            for s in self.source:
                try:
                    d=s.n3().split("/")[-1].replace(">","")
                    target_url = s.n3().replace(">","").replace("<","")
                    g = Graph()
                    g.parse(target_url)
                    comments.extend(self._get_comment(graph=g))
                except URLError as e:
                    print(f"URL is not resolved {e.strerror}")
            if len(comments)>1 :
                self.comments.append(comments[1].value)
            else:
                print(comments)

        def _get_comment(self,graph):
            pto = Namespace("http://www.productontology.org/id/")
            init_ns= {"pto":pto}
            sparql_query = """
                               SELECT ?y ?x 
                               WHERE {  ?y rdfs:comment  ?x .
                                        }"""
            query_result = graph.query(sparql_query,initNs=init_ns)
            return [row.x for row in query_result]

        def to_tuple(self):
            return self.label, self.source, self.subclasses, self.comments


class OntologyFIBOClient(Client):
    def __init__(self, config, path_key='fibo_path', path_entry_loans_key='fibo_entry_loans',path_entry_funds_key='fibo_entry_funds',
                 path_entry_fps_key='fibo_entry_fps'):
        super().__init__(config)
        self.funds=OntologyClient(self.config,path_key,path_entry_funds_key)
        self.loans=OntologyClient(self.config,path_key,path_entry_loans_key)
        self.fps=OntologyClient(self.config,path_key,path_entry_fps_key)
        self.funds_data = None
        self.loans_data = None
        self.fps_data = None
        self.get_data()


    def get_data(self):
        self.funds_data=self._get_funds()
        self.loans_data=self._get_loans()
        self.fps_data=self._get_fps()


    def _get_loans(self):
        return self._extract_data(self.loans)

    def _get_funds(self):
        return self._extract_data(self.funds)

    def _get_fps(self):
        return self._extract_data(self.fps)

    def _extract_data(self,ontology):
        labels = self._get_labels(ontology.graph)
        properties_labels = self._get_properties_labels(ontology.graph)
        class_properties_constraints = self._get_class_constraints(ontology.graph)
        subclasses = self._get_subclasses(ontology.graph)
        ontology_data = self._ontology_classes_factory(labels, properties_labels, class_properties_constraints,
                                                       subclasses)
        ontology.extracted_data = ontology_data
        return ontology_data

    def _get_labels(self, graph):
        sparql_query = """
                    SELECT ?y ?x 
                    WHERE {  
                             ?y rdf:type owl:Class . 
                             ?y rdfs:label ?x .
                             }"""
        query_result = graph.query(sparql_query)
        return [(row.y, row.x) for row in query_result]

    def _get_properties_labels(self,graph):
        sparql_query = """
                            SELECT ?y ?x 
                            WHERE {  
                                     ?y rdf:type owl:ObjectProperty .
                                     ?y rdfs:label ?x .
                                     }"""
        query_result = graph.query(sparql_query)
        return [(row.y, row.x) for row in query_result]

    def _get_class_constraints(self,graph):
        sparql_query = """
                                    SELECT ?y ?k ?x ?t ?z
                                    WHERE {  
                                             ?y rdf:type owl:Class .
                                             ?k owl:onProperty ?x .
                                             ?k owl:someValuesFrom ?z

                                             }"""
        query_result = graph.query(sparql_query)
        return [(row.y, row.x, row.z) for row in query_result]

    def _get_subclasses(self,graph):
        sparql_query = """
                    SELECT ?y ?x 
                    WHERE {  ?y rdf:type owl:Class .
                             ?y rdfs:subClassOf ?x .
                             }"""
        query_result = graph.query(sparql_query)
        return [(row.y, row.x) for row in query_result]

    def _ontology_classes_factory(self, labels, properties_labels, class_properties_constraints,subclasses):
        labels_dict = {}
        properties_labels_dict = {}
        subclasses_dict = {}
        for label in labels:
            labels_dict[label[0]] = label[1].value
        for property in properties_labels:
            properties_labels_dict[property[0]] = property[1].value
        for subclass in subclasses:
            uri = URIRef(subclass[1])
            if uri in labels_dict.keys() and subclass[0] in labels_dict.keys():
                if subclass[0] in subclasses_dict.keys():
                    subclasses_dict[labels_dict[subclass[0]]].append(labels_dict[uri])
                else:
                    subclasses_dict[labels_dict[subclass[0]]] = [labels_dict[uri]]
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
            if key in subclasses_dict.keys():
                ontology_data[key].subclasses = subclasses_dict[key]
            ontology_data[key].unique_values()
        return ontology_data

    class OntologyClass:
        def __init__(self, label):
            self.label = label
            self.properties_labels = []
            self.constraints = {}
            self.subclasses = []

        def unique_values(self):
            self.properties_labels = list(set(self.properties_labels))

        def to_tuple(self):
            return self.label, self.properties_labels, self.constraints, self.subclasses

