import json
import random,re
from random import sample
import pandas as pd

from s3lib.libclients import OpenAIClient, OntologyFIBOClient, OntologyGPOClient, OntologyECCFClient, \
    OntologyNACEClient, \
    CompaniesClient, CPEClient, OntologyPTOClient


class Landscape:
    def __init__(self, config,params=None, load_from_file=False,loaded_data=None):
        self.config = config
        self.load_from_file = load_from_file
        self.loaded_data = loaded_data
        self.parameters = params
        self.openai = OpenAIClient(config)

    def set_information_needs(self):
        pass

    @staticmethod
    def _decomposition(number, l, t=0):
        if t == 0:
            decomposition = [1] * l
        elif t == 1:
            decomposition = [0] * l
        else:
            decomposition = [1] * l
        remaining = number - l
        if remaining > 0:
            while remaining > 0:
                n = random.randint(1, remaining)
                index = random.randint(0, l - 1)
                decomposition[index] = decomposition[index] + n
                remaining -= n
        else:
            remaining = number
            while remaining > 0:
                n = random.randint(1, remaining)
                index = random.randint(0, l - 1)
                decomposition[index] = decomposition[index] + n
                remaining -= n
        return decomposition

    def _get_distribution(self, number, reference_list, t=0):
        distribution_d = self._decomposition(number, len(reference_list), t)
        return distribution_d


class InputLandscape(Landscape):
    """
    :parameter:
        params: a dictionary that defines the landscape parameters
                :params keys:
                        competitors_size: the number of competitors
                        competitors_industries: the industries on which competitors belongs
                        suppliers_size: the number of suppliers
                        suppliers_industries: the industries on which suppliers belongs
    """

    def __init__(self, config, params=None):
        super().__init__(config, params=params)
        self.competitors_industries_choice = self._get_industries_choices(params['competitors_industries'])
        self.suppliers_industries_choice = self._get_industries_choices(params['suppliers_industries'])
        self.suppliers_size = self._get_industries_size(params['suppliers_size'], self.suppliers_industries_choice)
        self.competitors_size = self._get_industries_size(params['competitors_size'],
                                                          self.competitors_industries_choice)
        self.companies = CompaniesClient(config)
        self.fibo = OntologyFIBOClient(config)
        self.suppliers = None
        self.competitors = None
        self.loans = None
        self.funds = None
        self.set_information_needs()


    def _get_industries_choices(self, industries_choice):
        if type(industries_choice) == list and len(industries_choice) > 0:
            industries_choices = industries_choice
        elif type(industries_choice) == int:
            industries_choices = random.sample(list(self.config['industries_choice'].keys()), industries_choice)
        else:
            industries_choices = random.sample(list(self.config['industries_choice'].keys()),
                                               random.randrange(len(list(self.config['industries_choice'].keys()))))
        return industries_choices

    @staticmethod
    def _get_industries_size(industries_size, industries_choice):
        if len(industries_choice) > industries_size:
            final_size = len(industries_choice) + 5
        else:
            final_size = industries_size
        return final_size

    def set_information_needs(self):
        if self.load_from_file:
            self.suppliers = self.loaded_data['suppliers']
            self.competitors = self.loaded_data['competitors']
            self.loans = self.loaded_data['loans']
            self.funds = self.loaded_data['funds']
        else:
            self._set_suppliers_information_needs()
            self._set_competitors_information_needs()
            self._set_capital_sources_information_needs()

    def _set_capital_sources_information_needs(self):

        loans_types = [value for key, value in self.fibo.loans_data.items() if
                       'loan' in value.label and len(value.subclasses) > 0]
        funds_types = [value for key, value in self.fibo.funds_data.items() if not (
                    'trust' in value.label or 'investment' in value.label or 'contract' in value.label or 'structure' in value.label or 'unit' in value.label)]
        if len(loans_types) > self.parameters['number_of_cs_loans']:
            loans_distribution = self._get_distribution(self.parameters['number_of_cs_loans'], loans_types, t=1)
        else:
            loans_distribution = self._get_distribution(self.parameters['number_of_cs_loans'], loans_types, t=0)
        if len(funds_types) > self.parameters['number_of_cs_funds']:
            funds_distribution = self._get_distribution(self.parameters['number_of_cs_funds'], funds_types, t=1)
        else:
            funds_distribution = self._get_distribution(self.parameters['number_of_cs_funds'], funds_types, t=0)
        loan_objects = self._choose_capital_source(loans_types, loans_distribution)
        fund_objects = self._choose_capital_source(funds_types, funds_distribution)
        self.loans = self._set_loans_information_needs(loan_objects)
        self.funds = self._set_funds_information_needs(fund_objects)

    @staticmethod
    def _choose_capital_source(loan_types, loans_distribution):
        capital_sources_objects = []
        for index in range(len(loans_distribution)):
            if loans_distribution[index] > 0:
                amount = loans_distribution[index]
                while amount > 0:
                    capital_sources_objects.append(loan_types[index])
                    amount -= 1
        return capital_sources_objects

    def _set_loans_information_needs(self, loan_objects):
        returned_data = []
        for l_obj in loan_objects:
            returned_data.append(self._create_loan_information_needs(l_obj))
        return returned_data

    def _create_loan_information_needs(self, l_obj):
        message1 = f"Give me an example of {l_obj.to_tuple()[0]} and return the result as a json file. Then, tell me what cyber threats exist against those type of loans"
        response1 = self.openai.call_openai(message1)
        return response1

    def _set_funds_information_needs(self, funds_objects):
        returned_data = []
        for f_obj in funds_objects:
            returned_data.append(self._create_funds_information_needs(f_obj))
            break
        return returned_data

    def _create_funds_information_needs(self, f_obj):
        message1 = f"Give me an example of {f_obj.to_tuple()[0]} and return the result as a json file. Then, tell me what cyber threats exist against those type of funds"
        response1 = self.openai.call_openai(message1)
        return response1

    def _set_suppliers_information_needs(self):
        self.suppliers = self._set_companies_information_needs(self.suppliers_industries_choice, self.suppliers_size)

    def _set_competitors_information_needs(self):
        self.competitors = self._set_companies_information_needs(self.competitors_industries_choice,
                                                                 self.competitors_size, ctype=1)

    def _set_companies_information_needs(self, industries_choice, industries_size, ctype=0):
        industries_distribution = self._get_distribution(industries_size, industries_choice)
        companies = self.companies.get_companies_sample(industries_distribution[0],
                                                        self.config['industries_choice'][industries_choice[0]])
        for i in range(1, len(industries_distribution)):
            companies1 = self.companies.get_companies_sample(industries_distribution[i],
                                                             self.config['industries_choice'][industries_choice[i]])
            companies = pd.concat([companies, companies1])
        return self._create_companies_information_needs(companies, ctype)

    def _create_companies_information_needs(self, companies, ctype):
        returned_data = {}
        for index, row in companies.iterrows():
            returned_data[index] = self._create_company_information_needs(row, ctype)
        return returned_data

    def _create_company_information_needs(self, row, ctype):
        fields = [row['handle'], row['name'], row['domain'], row['website'], row['industry'], row['type'], row['city'],
                  row['state']]
        response = []
        # Generic Messages
        message0 = f"What should I know about {row['name']} which has the website {row['website']} and is located in {row['city']}"
        response.append(self.openai.call_openai(message0))
        if ctype == 0:
            # Suppliers
            response.extend(self._supplier_information_needs(row))
        elif ctype == 1:
            # Competititors
            response.extend(self._competitor_information_needs(row))
        return response

    def _supplier_information_needs(self, row):
        response = []
        message0 = f"What cyber incidents are related to {row['name']} with website {row['website']}"
        response.append(self.openai.call_openai(message0))
        message1 = f"What are the products of the company {row['name']} with website {row['website']}"
        response.append(self.openai.call_openai(message1))
        return response

    def _competitor_information_needs(self, row):
        response = []
        message0 = f"What cyber incidents are related to the products of {row['name']} with website {row['website']}"
        response.append(self.openai.call_openai(message0))
        message1 = f"What are business areas of the company {row['name']} with website {row['website']}"
        response.append(self.openai.call_openai(message1))
        return response



class TransformationProcessLandscape(Landscape):

    def __init__(self, config,params):
        super().__init__(config,params=params)
        self.nace = OntologyNACEClient(config)
        self.gpo = OntologyGPOClient(config)
        self.cpe = CPEClient(config)
        self.business_activities_choice= self._get_business_activities_choice(self.parameters['business_activities_choice'])
        self.business_activities_size = self._get_business_activities_size(self.parameters['business_activities_size'],
                                                          self.business_activities_choice)
        self.business_activities=None
        self.internal_operations=None
        self.information_systems=None
        self.set_information_needs()

    def _get_business_activities_choice(self,business_activities_choice):
        if type(business_activities_choice) == list and len(business_activities_choice) > 0:
            business_activities_choices = business_activities_choice
        elif type(business_activities_choice) == int:
            business_activities_choices = random.sample(list(self.config['business_activities_choice'].keys()), business_activities_choice)
        else:
            business_activities_choices = random.sample(list(self.config['business_activities_choice'].keys()),
                                                   random.randrange(len(list(self.config['business_activities_choice'].keys()))))
        return business_activities_choices


    @staticmethod
    def _get_business_activities_size(business_activities_size, business_activities_choice):
        if len(business_activities_choice) > business_activities_size:
            final_size = len(business_activities_choice) + 5
        else:
            final_size = business_activities_size
        return final_size

    def set_information_needs(self):
        #self.business_activities=self._set_business_activities_information_needs()
        #self.internal_operations=self._set_internal_operations_information_needs()
        self.information_systems=self._set_information_systems_information_needs()



    def _set_business_activities_information_needs(self):
        nace_cleaned_data=[]
        for key in self.nace.loadeddata.data.keys():
            if 'prefLabel' in self.nace.loadeddata.data[key].keys():
                nace_cleaned_data.append(self.nace.loadeddata.data[key])

        business_activities_distribution=self._get_distribution(self.business_activities_size,self.business_activities_choice)


        chosen_business_activities=self._get_business_area_activities(nace_cleaned_data,business_activities_distribution)

        business_activities_information_needs=self._create_business_activities_information_needs(chosen_business_activities)
        return business_activities_information_needs

    def _create_business_activities_information_needs(self,business_activities):
        information_needs=[]
        for ba in business_activities:
            information_needs.extend(self._create_internal_operation_information_needs(ba))
        return information_needs

    def _create_business_activity_information_needs(self,business_activity):
        response = []
        message0 = f"What should I know about {business_activity[0]} with a description as {business_activity[1]}"
        message1 = f"What cyber threats are related to {business_activity[0]}?"
        response.append(self.openai.call_openai(message0))
        response.append(self.openai.call_openai(message1))
        return response

    def _get_business_area_activities(self,business_activities,activities_distribution):
        returned_data = []
        t=0
        for index in self.business_activities_choice:
            idx=self.business_activities_choice.index(index)
            returned_activities, t =self._get_business_activities(business_activities[index],activities_distribution[idx]+t)
            returned_data.extend(returned_activities)
        return returned_data

    @staticmethod
    def _get_business_activities(business_area, size):
        narrower_concepts=business_area['narrower_concepts']
        narrower_concepts_data=business_area['narrower_concepts_data']
        concepts={}
        for nr_concept in narrower_concepts:
            for nr_concept_data in narrower_concepts_data:
                if nr_concept in nr_concept_data.keys():
                    fl_narrower_concepts=nr_concept_data[nr_concept][nr_concept]
                    fl_narrower_concepts_data=nr_concept_data[nr_concept]['first_level_narrower_concepts_data']
                    for fl_nr_concept in fl_narrower_concepts:
                        for fl_nr_concept_data in fl_narrower_concepts_data:
                            if fl_nr_concept in fl_nr_concept_data.keys():
                                if 'prefLabel' in fl_nr_concept_data[fl_nr_concept].keys():
                                    concepts[fl_nr_concept]=(fl_nr_concept_data[fl_nr_concept]['prefLabel'],fl_nr_concept_data[fl_nr_concept]['definition'])
        if len(list(concepts.keys()))>size:
            sample_a=random.sample(list(concepts.keys()),size)
            t=0
        else:
            t=size-len(list(concepts.keys()))
            sample_a=random.sample(list(concepts.keys()),len(list(concepts.keys())))
        returned_activities=[]
        for s in sample_a:
            returned_activities.append(concepts[s])
        return returned_activities,t

        #sample = random.sample(business_activities[index]['narrower_concepts'], activities_distribution[idx])
        #print(sample)
        #print(business_activities[index])
        # print(business_activities[index])


    def _set_internal_operations_information_needs(self):
        operations=self._get_internal_operations()
        information_needs=self._create_internal_operations_information_needs(operations)
        return information_needs


    def _create_internal_operations_information_needs(self,operations):
        information_needs=[]
        for operation in operations:
            information_needs.extend(self._create_internal_operation_information_needs(operation))
        return information_needs

    def _create_internal_operation_information_needs(self,operation):
        response = []
        message0 = f"What should I know about {operation[0]}?"
        message1 = f"What cyber threats are related to {operation[1]}?"
        response.append(self.openai.call_openai(message0))
        response.append(self.openai.call_openai(message1))
        return response

    def _get_internal_operations(self):
        gpo=self.gpo.get_data()
        cleaned_operations=[]
        for e in gpo.keys():
            if 'Process' in gpo[e].label:
                cleaned_operations.append(gpo[e].to_tuple())
        sample_operations=random.sample(cleaned_operations,self.parameters['number_of_internal_operations'])
        return sample_operations


    def _set_information_systems_information_needs(self):
        information_systems=self._get_information_systems()
        information_needs=self._create_information_systems_information_needs(information_systems)
        print(information_needs)
        return information_needs

    def _get_information_systems(self):
        chosen_information_systems= random.sample(self.cpe.extracted_data,self.parameters['number_of_information_systems'])
        return chosen_information_systems

    def _create_information_systems_information_needs(self,information_systems):
        information_needs=[]
        for information_system in information_systems:
            information_needs.extend(self._create_information_system_information_needs(information_system))
        return information_needs

    def _create_information_system_information_needs(self,information_system):
        response = []
        message0 = f"What should I know about {information_system.title}?"
        message1 = f"What cyber threats are related to {information_system.title}?"
        response.append(self.openai.call_openai(message0))
        response.append(self.openai.call_openai(message1))
        return response


class OutputLandscape(Landscape):

    def __init__(self, config,params=None):
        super().__init__(config,params=params)
        self.pto = OntologyPTOClient(config)
        self.eccf = OntologyECCFClient(config)
        self.products=None
        self.services=None
        self.set_information_needs()

    def set_information_needs(self):
        self.products=self._set_products_information_needs()
        self.services=self._set_services_information_needs()

    def _set_products_information_needs(self):
        products=self._get_products()
        information_needs= self._create_products_information_needs(products)
        return information_needs

    def _get_products(self):
        sample_products=[]
        sample_product_keys=random.sample(list(self.pto.loadeddata.data.keys()),self.parameters['number_of_products'])
        for key in sample_product_keys:
            sample_products.append(self.pto.loadeddata.data[key])
        return sample_products

    def _create_products_information_needs(self,products):
        information_needs=[]
        for product in products:
            information_needs.extend(self._create_product_information_needs(product))
        return information_needs

    def _create_product_information_needs(self,product):
        response = []
        message0 = f"What should I know about {product[0]}?"
        message1 = f"What cyber threats are related to {product[0]}?"
        response.append(self.openai.call_openai(message0))
        response.append(self.openai.call_openai(message1))
        return response

    def _set_services_information_needs(self):
        services= self._get_services()
        information_needs=self._create_services_information_needs(services['services'])
        return information_needs

    def _get_services(self):
        service_obj=None
        for key in self.eccf.extracted_data.keys():
            if 'Service' in self.eccf.extracted_data[key].label:
                service_obj=self.eccf.extracted_data[key]
        constraints_string=""
        for key in service_obj.constraints.keys():
            constraints_string+=f"{key}  {service_obj.constraints[key]},\n"

        string_query=f"Give {self.parameters['number_of_services']} examples of {service_obj.label} which {constraints_string} , return the result in json format"
        response = self.openai.call_openai(string_query)
        return self._construct_service(response)

    @staticmethod
    def _construct_service(response):
        data=response.split('```')
        data = json.loads(data[1].replace('json',''))
        return data


    def _create_services_information_needs(self,services):
        information_needs=[]
        for service in services:
            text_service=f""
            for key in service.keys():
                text_service+=f"{key}  {service[key]},\n"
            information_needs.extend(self._create_service_information_needs(text_service))
        return information_needs

    def _create_service_information_needs(self,service):
        response = []
        message0 = f"What should I know about {service}?"
        message1 = f"What cyber threats are related to {service}?"
        response.append(self.openai.call_openai(message0))
        response.append(self.openai.call_openai(message1))
        return response



