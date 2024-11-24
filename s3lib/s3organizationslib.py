import os, json

from openai import organization

from s3lib.relevance.s3landscapeslib import InputLandscape, TransformationProcessLandscape, OutputLandscape


class Organization:


    def __init__(self, name, config, params, load_from_file=False):
        self.name = name
        self.config = config
        self.params = params
        self.load_from_file = load_from_file
        self.paths = None
        if self.load_from_file:
            print(f"Loading organization {self.name}...")
        else:
            print(f"Creating organization {self.name}...")

    def _create_paths(self):
        pass

    def _write_organization(self):
        pass

    @staticmethod
    def _load_data(filepath):
        with open(filepath, 'r') as f:
            json_data = json.load(f)
        return json_data

    @staticmethod
    def _write_data(filepath, data):
        with open(filepath, 'w') as f:
            json_object = json.dumps(data, indent=4)
            f.write(json_object)


class OrganizationRelevance(Organization):

    def __init__(self, name, config, params, load_from_file=False):
        super().__init__(name, config, params, load_from_file)
        self.paths = self._create_paths()
        if load_from_file:
            print(f"Loading organization {self.name}")
            organization_data=self._load_data(f"{self.paths['organization_path']}\\{self.name}.json")
            print(f"Loading organization {self.name} : Input Landscape")
            self.input_landscape = InputLandscape(self.config, self.params,self.load_from_file,organization_data)
            print(f"Loading organization {self.name} : Transformation Process Landscape")
            self.transformation_process_landscape = TransformationProcessLandscape(self.config, self.params,self.load_from_file,organization_data)
            print(f"Loading organization {self.name} : Output Landscape")
            self.output_landscape = OutputLandscape(self.config, self.params,self.load_from_file,organization_data)
        else:
            print(f"Creating organization {self.name} : Input Landscape")
            self.input_landscape = InputLandscape(self.config, self.params)
            print(f"Creating organization {self.name} : Transformation Process Landscape")
            self.transformation_process_landscape = TransformationProcessLandscape(self.config, self.params)
            print(f"Creating organization {self.name} : Output Landscape")
            self.output_landscape = OutputLandscape(self.config, self.params)
            self._write_organization()

    def _create_paths(self):
        organization_path = self.config[self.name]
        landscape_li_path = os.path.join(organization_path, self.config["landscape_li"])
        landscape_li_capital_sources_path = os.path.join(str(landscape_li_path), "capital_sources")
        landscape_li_competitors_path = os.path.join(str(landscape_li_path), "competitors")
        landscape_li_suppliers_path = os.path.join(str(landscape_li_path), "suppliers")
        landscape_lo_path = os.path.join(organization_path, self.config["landscape_lo"])
        landscape_lo_products_path = os.path.join(str(landscape_lo_path), "products")
        landscape_lo_services_path = os.path.join(str(landscape_lo_path), "services")
        landscape_ltp_path = os.path.join(organization_path, self.config["landscape_ltp"])
        landscape_ltp_business_activities_path = os.path.join(str(landscape_ltp_path), "business_activities")
        landscape_ltp_information_systems_path = os.path.join(str(landscape_ltp_path), "information_systems")
        landscape_ltp_internal_operations_path = os.path.join(str(landscape_ltp_path), "internal_operations")
        return {'organization_path': organization_path, 'landscape_li_path': landscape_li_path,
                'landscape_li_capital_sources_path': landscape_li_capital_sources_path,
                'landscape_li_competitors_path': landscape_li_competitors_path,
                'landscape_li_suppliers_path': landscape_li_suppliers_path, 'landscape_lo_path': landscape_lo_path,
                'landscape_lo_products_path': landscape_lo_products_path, 'landscape_ltp_path': landscape_ltp_path,
                'landscape_lo_services_path': landscape_lo_services_path,
                'landscape_ltp_business_activities_path': landscape_ltp_business_activities_path,
                'landscape_ltp_information_systems_path': landscape_ltp_information_systems_path,
                'landscape_ltp_internal_operations_path': landscape_ltp_internal_operations_path}

    def _write_organization(self):
        data = {'suppliers': self.input_landscape.suppliers, 'competitors': self.input_landscape.competitors,
                'loans': self.input_landscape.loans, 'funds': self.input_landscape.funds,
                'business_activities': self.transformation_process_landscape.business_activities,
                'internal_operations': self.transformation_process_landscape.internal_operations,
                'information_systems': self.transformation_process_landscape.information_systems,
                'products': self.output_landscape.products, 'services': self.output_landscape.services}
        print(f"Writing organization {self.name} to files...")
        self._write_landscapes()
        self._write_data(f"{self.paths['organization_path']}\\{self.name}.json", data)

    def _write_landscapes(self):
        self._write_data(f"{self.paths['landscape_li_capital_sources_path']}\\{self.name}_funds.json",
                         self.input_landscape.funds)
        self._write_data(f"{self.paths['landscape_li_capital_sources_path']}\\{self.name}_loans.json",
                         self.input_landscape.loans)
        self._write_data(f"{self.paths['landscape_li_competitors_path']}\\{self.name}_competitors.json",
                         self.input_landscape.competitors)
        self._write_data(f"{self.paths['landscape_li_suppliers_path']}\\{self.name}_suppliers.json",
                         self.input_landscape.suppliers)
        self._write_data(f"{self.paths['landscape_lo_products_path']}\\{self.name}_products.json",
                         self.output_landscape.products)
        self._write_data(f"{self.paths['landscape_lo_services_path']}\\{self.name}_services.json",
                         self.output_landscape.services)
        self._write_data(
            f"{self.paths['landscape_ltp_business_activities_path']}\\{self.name}_business_activities.json",
            self.transformation_process_landscape.business_activities)
        self._write_data(
            f"{self.paths['landscape_ltp_internal_operations_path']}\\{self.name}_internal_operations.json",
            self.transformation_process_landscape.internal_operations)
        self._write_data(
            f"{self.paths['landscape_ltp_information_systems_path']}\\{self.name}_information_systems.json",
            self.transformation_process_landscape.information_systems)


class OrganizationActionability(Organization):

    def __init__(self, name, config, params, load_from_file=False):
        super().__init__(name, config, params, load_from_file)
        self.paths = self._create_paths()
        self.k_sets=self.params['k_sets']
        self.cti_products_number=self.params['cti_products_number']
        self.products_per_k_set=self.params['products_per_k_set']
        #print(f"Organization {self.name} has {self.k_sets} defence mechanisms, knowledge base of {self.cti_products_number} cti products , with {self.products_per_k_set} per mechanism")
        if load_from_file:
            print(f"Loading organization {self.name}")
        else:
            print(f"Creating organization {self.name} defence mechanisms")
            #self._write_organization()

    def _write_organization(self):

        pass

