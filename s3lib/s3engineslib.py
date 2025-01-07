import nltk

class Engine:
    def __init__(self,config,organization,product):
        self.config = config
        self.organization = organization
        self.product = product
        self.engine_core =None

    def get_metric(self):
        pass

    def set_cti_product(self,cti_product):
        self.product = cti_product

class EngineCore:
    def __init__(self,config,product):
        self.config = config
        self.product = product
        nltk.download('stopwords')
        nltk.download('wordnet')

    def calculate_metric(self):
        pass

