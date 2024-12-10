from s3lib.s3engineslib import Engine, EngineCore
from datasketch import MinHash
from statistics import mean
from s3lib.s3functions import clean_dict,clean_text



class RelevanceMetricEngine(Engine):

    def __init__(self,config,target_organization=None, cti_product=None):
        super().__init__(config,target_organization,cti_product)
        landscapes=[self.calculate_input_landscape(),self.calculate_output_landscape(),self.calculate_transformation_process_landscape()]

        self.engine_core=self.RelevanceMetricCore(self.config,self.product,landscapes)

    def _set_organization(self,target_organization):
        self.organization = target_organization

    def _set_product(self,cti_product):
        self.product = cti_product

    def get_metric(self):
        return self.engine_core.calculate_metric()

    def calculate_input_landscape(self):
        input_landscape = self.organization.input_landscape
        suppliers = self._clean_suppliers(input_landscape.suppliers)
        competitors = self._clean_competitors(input_landscape.competitors)
        loans = self._clean_loans(input_landscape.loans)
        funds = self._clean_funds(input_landscape.funds)
        landscape = []
        landscape.extend(suppliers)
        landscape.extend(competitors)
        landscape.extend(loans)
        landscape.extend(funds)
        landscape = set(landscape)
        return landscape

    def _clean_funds(self, funds):
        cleaned_funds = []
        text_funds = ""
        for fund in funds:
            fund_split = fund.split('```')
            for fund_split_part in fund_split:
                if fund_split_part.startswith('json'):
                    data = clean_dict(fund_split_part.replace("json", ""))
                    text_funds += data
                elif 'threats' in fund_split_part.lower():
                    text_funds += fund_split_part
        cleaned_funds.extend(clean_text(text_funds))
        return cleaned_funds

    def _clean_loans(self, loans):
        cleaned_loans = []
        text_loans = ""
        for loan in loans:
            loan_split = loan.split('```')
            for loan_split_part in loan_split:
                if loan_split_part.startswith('json'):
                    data = clean_dict(loan_split_part.replace("json", ""))
                    text_loans += data
                elif 'threats' in loan_split_part.lower():
                    text_loans += loan_split_part
        cleaned_loans.extend(clean_text(text_loans))
        return cleaned_loans

    def _clean_competitors(self, competitors):
        cleaned_competitor = ""
        for key in competitors.keys():
            competitor = competitors[key]
            doc_competitor = ""
            for info_part in competitor:
                doc_competitor += info_part
            cleaned_competitor += doc_competitor
        return clean_text(cleaned_competitor)

    def _clean_suppliers(self, suppliers):
        cleaned_suppliers = ""
        for key in suppliers.keys():
            supplier = suppliers[key]
            doc_supplier = ""
            for info_part in supplier:
                doc_supplier += info_part
            cleaned_suppliers += doc_supplier
        return clean_text(cleaned_suppliers)

    def calculate_output_landscape(self):
        output_landscape = self.organization.output_landscape
        products = self._clean_products(output_landscape.products)
        services = self._clean_services(output_landscape.services)
        landscape = []
        landscape.extend(products)
        landscape.extend(services)
        landscape = set(landscape)
        return landscape

    def _clean_services(self, services):
        cleaned_services = []
        doc_services = ""
        for service in services:
            doc_services += service
        cleaned_services.extend(clean_text(doc_services))
        return cleaned_services

    def _clean_products(self, products):
        cleaned_products = []
        doc_products = ""
        for product in products:
            doc_products += product
        cleaned_products.extend(clean_text(doc_products))
        return cleaned_products

    def calculate_transformation_process_landscape(self):
        transformation_process_landscape = self.organization.transformation_process_landscape
        business_activities = self._clean_business_activities(transformation_process_landscape.business_activities)
        internal_operations = self._clean_internal_operations(transformation_process_landscape.internal_operations)
        information_systems = self._clean_information_systems(transformation_process_landscape.information_systems)
        landscape = []
        landscape.extend(business_activities)
        landscape.extend(internal_operations)
        landscape.extend(information_systems)
        landscape = set(landscape)
        return landscape

    def _clean_information_systems(self, information_systems):
        cleaned_information_systems = []
        doc_information_system = ""
        for information_system in information_systems:
            doc_information_system += information_system
        cleaned_information_systems.extend(clean_text(doc_information_system))
        return cleaned_information_systems

    def _clean_internal_operations(self, internal_operations):
        cleaned_internal_operations = []
        doc_operations = ""
        for operation in internal_operations:
            doc_operations += operation
        cleaned_internal_operations.extend(clean_text(doc_operations))
        return cleaned_internal_operations

    def _clean_business_activities(self, business_activities):
        cleaned_business_activities = []
        doc_activities = ""
        for activity in business_activities:
            doc_activities += activity
        cleaned_business_activities.extend(clean_text(doc_activities))
        return cleaned_business_activities






    class RelevanceMetricCore(EngineCore):
        def __init__(self,config,cti_product,landscapes):
            super().__init__(config,cti_product)
            self.landscapes=landscapes

        def calculate_metric(self):
            minhash_list=[]
            for landscape in self.landscapes:
                minhash_list.append(self._compute_minhash(landscape))

            #TODO minhash CTI
            #minhash_cti=self._compute_minhash(self.product)
            #comparison_results_list=[]
            #for minhash in minhash_list:
            #    comparison_results_list.append(self._jaccard_similarity(minhash,minhash_cti))

            return mean([1,1,1])

        @staticmethod
        def _compute_minhash(landscape, num_perm=128):
            """
            Computes the MinHash signature for a set of tokens using the datasketch library.

            :param tokens: an iterable of hashable tokens (e.g., words in a document)
            :param num_perm: number of permutations/hashes to use for the MinHash
            :return: a MinHash object representing the signature
            """
            minhash = MinHash(num_perm=num_perm)
            for token in landscape:
                minhash.update(token.encode('utf8'))
            return minhash

        @staticmethod
        def _jaccard_similarity(self,minhash1, minhash2):
            """
            Computes the Jaccard similarity between two MinHash objects.

            :param minhash1: The first MinHash object
            :param minhash2: The second MinHash object
            :return: The Jaccard similarity between the two MinHash signatures
            """
            return minhash1.jaccard(minhash2)