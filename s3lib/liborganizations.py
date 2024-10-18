from s3lib.relevance.s3landscapeslib import InputLandscape


class Organization:
    def __init__(self, name,config,params):
        self.name = name
        self.config = config
        self.params = params

    def _load_data(self):
        pass

    def _write_data(self):
        pass

class OrganizationRelevance(Organization):

    def __init__(self, name,config,params):
        super().__init__(name,config,params)
        self.input_landscape=InputLandscape(self.config, self.params)

class OrganizationActionability(Organization):

    def __init__(self, name,config,params):
        super().__init__(name,config,params)
