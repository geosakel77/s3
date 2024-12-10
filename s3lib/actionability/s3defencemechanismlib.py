from s3lib.s3clientslib import OpenCTIClient
import random

class DefenceMechanism:

    def __init__(self, config,name,number_of_products,load_from_file=False):
        #self.open_cti_client = OpenCTIClient(config)
        self.name = name
        self.number_of_products = number_of_products
        if not load_from_file:
            self.knowledge_base=self._create_knowledge_base()

    def _create_knowledge_base(self):
        knowledge_base=[]
        for i in range(self.number_of_products):
            #TODO
            #knowledge_base.append(self.open_cti_client.get_malware())
            knowledge_base.append(random.randint(1,self.number_of_products))
        return knowledge_base

    def get_knowledge_base(self):
        return self.knowledge_base

    def set_knowledge_base(self,knowledge_base):
        self.knowledge_base=knowledge_base

