import multiprocessing
from s3lib.s3organizationslib import OrganizationRelevance
from config.config import prepare_relevance_metric_config

def create_organization(name,config,parameters):
    organization = OrganizationRelevance(name,config,parameters)
    return organization


def prepare_relevance_metric_env(config):
    print(f"Starting the relevance metric experimental environment preparation...")
    organizations_names,organizations_conf = prepare_relevance_metric_config()
    items = []
    for organization_name in organizations_names:
        items.append((organization_name,config,organizations_conf[organization_name]))
    try:
        with multiprocessing.Pool(processes=2,maxtasksperchild=6) as pool:
            for result in pool.starmap(create_organization, items):
                print(result)
    except Exception as e:
        print(e)

    print(f"End of the experimental environment preparation")
