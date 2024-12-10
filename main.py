from config.config import read_config,prepare_relevance_metric_config,prepare_actionability_metric_config
from s3lib.s3organizationslib import OrganizationRelevance, OrganizationActionability
from s3lib.relevance.s3relevancelib import RelevanceMetricEngine
from s3lib.actionability.s3actionabilitylib import ActionabilityMetricEngine
from s3lib.s3clientslib import OpenCTIClient, MandiantCTIClient


def run_relevance_metric_experiments(config):
    organizations_names, organizations_conf = prepare_relevance_metric_config()
    print("Loading the relevance metric organizations ..... ")
    organizations = {}
    for organization_name in organizations_names:
        print(f"Loading organization {organization_name}...")
        organization = OrganizationRelevance(name=organization_name, config=config,
                                             params=organizations_conf[organization_name], load_from_file=True)
        organizations[organization_name] = organization

    sample_cti = "ddsdsdsds fsffdfdf sfdfdfd"
    for organization_name in organizations.keys():
        engine = RelevanceMetricEngine(config, organizations[organization_name], sample_cti)
        print(engine.get_metric())

def run_actionability_metric_experiments(config):
    organizations_names, organizations_conf = prepare_actionability_metric_config()
    print("Loading the actionability metric organizations ..... ")
    organizations = {}
    for organization_name in organizations_names:
        print(f"Loading organization {organization_name}...")
        organization = OrganizationActionability(name=organization_name, config=config,
                                             params=organizations_conf[organization_name], load_from_file=True)
        organizations[organization_name] = organization

    sample_cti = "ddsdsdsds fsffdfdf sfdfdfd"
    for organization_name in organizations.keys():
        engine = ActionabilityMetricEngine(config, organizations[organization_name], sample_cti)
        print(engine.get_metric())

def run():
    config = read_config("config/config.ini")

    print(f"Starting the experiment...")
    #run_relevance_metric_experiments(config)
    #run_actionability_metric_experiments(config)

    test_client= MandiantCTIClient(config)#OpenCTIClient(config)
    test_reports=test_client.get_reports()

    for report in test_reports:
        print(report.report_id)

    #print(test_client.get_malware("linux"))
    #print(test_client.get_report("windows"))

    print(f"End of the experimental environment preparation")





# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    run()
