import nltk

class Engine:
    def __init__(self,config,organization,product):
        self.config = config
        self.organization = organization
        self.product = product
        self.engine_core =None


class EngineCore:
    def __init__(self,config,organization,product):
        self.config = config
        self.organization = organization
        self.product = product
        nltk.download('stopwords')
        nltk.download('wordnet')

    def calculate_metric(self):
        pass

