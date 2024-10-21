import os
from s3lib.relevance.s3landscapeslib import InputLandscape, TransformationProcessLandscape, OutputLandscape


class Organization:
    def __init__(self, name,config,params,load_from_file=False):
        self.name = name
        self.config = config
        self.params = params
        self.load_from_file = load_from_file
        self.context=None
        self.paths = self._create_paths()

    def _create_paths(self):
        organization_path = self.config[self.name]
        landscape_li_path = os.path.join(organization_path, self.config["landscape_li"])
        landscape_li_capital_sources_path = os.path.join(str(landscape_li_path), "capital_sources")
        landscape_li_competitors_path = os.path.join(str(landscape_li_path), "competitors")
        landscape_li_suppliers_path = os.path.join(str(landscape_li_path), "suppliers")
        landscape_lo_path = os.path.join(organization_path, self.config["landscape_lo"])
        landscape_lo_products_path = os.path.join(str(landscape_lo_path), "products")
        landscape_lo_competitors_path = os.path.join(str(landscape_lo_path), "services")
        landscape_ltp_path = os.path.join(organization_path, self.config["landscape_ltp"])
        landscape_ltp_business_activities_path = os.path.join(str(landscape_ltp_path), "business_activities")
        landscape_ltp_information_systems_path = os.path.join(str(landscape_ltp_path), "information_systems")
        landscape_ltp_internal_operations_path = os.path.join(str(landscape_ltp_path), "internal_operations")
        return {'organization_path':organization_path,'landscape_li_path':landscape_li_path,'landscape_li_capital_sources_path':landscape_li_capital_sources_path,
                'landscape_li_competitors_path':landscape_li_competitors_path,'landscape_li_suppliers_path':landscape_li_suppliers_path,'landscape_lo_path':landscape_lo_path,
                'landscape_lo_products_path':landscape_lo_products_path,'landscape_ltp_path':landscape_ltp_path,'landscape_lo_competitors_path':landscape_lo_competitors_path,
                'landscape_ltp_business_activities_path':landscape_ltp_business_activities_path,'landscape_ltp_information_systems_path':landscape_ltp_information_systems_path,
                'landscape_ltp_internal_operations_path':landscape_ltp_internal_operations_path}


    def _load_data(self):
        pass

    def _write_data(self):
        pass

class OrganizationRelevance(Organization):

    def __init__(self, name,config,params,paths,load_from_file=False):
        super().__init__(name,config,params,paths,load_from_file)
        if load_from_file:
            pass
        else:
            self.input_landscape=InputLandscape(self.config, self.params)
            self.transformation_process_landscape=TransformationProcessLandscape(self.config, self.params)
            self.output_landscape=OutputLandscape(self.config, self.params)



class OrganizationActionability(Organization):

    def __init__(self, name,config,params,paths,load_from_file=False):
        super().__init__(name,config,params,paths,load_from_file)
