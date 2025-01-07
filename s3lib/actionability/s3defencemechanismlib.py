from s3lib.s3clientslib import LocalCTIClient
import random

class DefenceMechanism:

    def __init__(self, config,name,number_of_products,load_from_file=False,loaded_knowledge_base=None):
        self.open_cti_client = None
        self.name = name
        self.number_of_products = number_of_products
        if not load_from_file:
            self.open_cti_client = LocalCTIClient(config, raw_data_client=False)
            self.knowledge_base=self._create_knowledge_base()
        else:
            self.knowledge_base=loaded_knowledge_base

    def _create_knowledge_base(self):
        knowledge_base={}
        keys = self.open_cti_client.cti_data.keys()
        selected_keys = random.sample(sorted(keys), self.number_of_products)
        for key in selected_keys:
            knowledge_base[key]=self.open_cti_client.cti_data[key]
        return knowledge_base

    def get_knowledge_base(self):
        return self.knowledge_base

    def set_knowledge_base(self,knowledge_base):
        self.knowledge_base=knowledge_base

