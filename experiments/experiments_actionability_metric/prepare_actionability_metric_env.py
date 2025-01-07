from s3lib.s3organizationslib import OrganizationActionability
from config.config import prepare_actionability_metric_config

def create_organization(name,config,parameters):
    organization = OrganizationActionability(name,config,parameters)
    return organization


def prepare_actionability_metric_env(config):
    print(f"Starting the actionability metric experimental environment preparation...")
    organizations_names,organizations_conf = prepare_actionability_metric_config()
    items = []
    for organization_name in organizations_names:
        organization = create_organization(organization_name,config,organizations_conf[organization_name])
        items.append(organization)
    print(f"End of the experimental environment preparation")


