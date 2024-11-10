from s3lib.s3engineslib import Engine, EngineCore
from datasketch import MinHash
from statistics import mean

class RelevanceMetricEngine(Engine):

    def __init__(self,config,target_organization=None, cti_product=None):
        super().__init__(config,target_organization,cti_product)
        self.engine_core=self.RelevanceMetricCore(self.config,self.organization,self.product)

    def _set_organization(self,target_organization):
        self.organization = target_organization

    def _set_product(self,cti_product):
        self.product = cti_product

    def get_metric(self):
        return self.engine_core.calculate_metric()


    class RelevanceMetricCore(EngineCore):
        def __init__(self,config,target_organization, cti_product):
            super().__init__(config,target_organization,cti_product)

        def calculate_metric(self):
            return mean([self.calculate_output_landscape_minhash(),self.calculate_input_landscape_minhash(),self.calculate_transformation_process_landscape()])

        def calculate_input_landscape_minhash(self):
            input_landscape = self.organization.input_landscape
            print(input_landscape.suppliers)
            #TODO
            return 1

        def calculate_output_landscape_minhash(self):
            return 1

        def calculate_transformation_process_landscape(self):
            return 1