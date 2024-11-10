from http.client import responses

from stix2validator.v21.musts import process

from config.config import read_config
from config.orgprofilesconf import *
from s3lib.s3organizationslib import OrganizationRelevance
from s3lib.relevance.s3relevancelib import RelevanceMetricEngine

def run():

    print(f"Starting the experiment...")
    print("Reading the experiment configuration...")
    CONFIG = read_config("config/config.ini")
    print(f"Reading the organizations configuration..")
    organizations_names = ['c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'c10']
    organizations_conf = {'c1': C1, 'c2': C2, 'c3': C3, 'c4': C4, 'c5': C5, 'c6': C6, 'c7': C7, 'c8': C8, 'c9': C9,
                          'c10': C10}
    print("Loading the organizations ..... ")
    organizations={}
    for organization_name in organizations_names:
        print(f"Loading organization {organization_name}...")
        organization = OrganizationRelevance(name=organization_name, config=CONFIG,
                                             params=organizations_conf[organization_name],load_from_file=True)
        organizations[organization_name] = organization
        break

    sample_cti="ddsdsdsds fsffdfdf sfdfdfd"
    for organization_name in organizations.keys():
        engine=RelevanceMetricEngine(CONFIG,organizations[organization_name],sample_cti)
        print(engine.get_metric())
        
    print(f"End of the experimental environment preparation")





# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    run()
