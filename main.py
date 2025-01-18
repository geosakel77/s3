from config.config import read_config,prepare_relevance_metric_config,prepare_actionability_metric_config
from s3lib.s3organizationslib import OrganizationRelevance, OrganizationActionability
from s3lib.relevance.s3relevancelib import RelevanceMetricEngine
from s3lib.actionability.s3actionabilitylib import ActionabilityMetricEngine
from s3lib.s3statisticslib import prepare_data_rel, prepare_data_act, plot_products_metric_comparison,plot_distributions_violin, plot_bar_distribution
import os, json,random

def write_data(filepath, data):
    with open(filepath, 'w') as f:
        json_object = json.dumps(data, indent=4)
        f.write(json_object)

def load_data(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)
    return data

def load_validation_data(config):
    filepath=config['validation_dataset']
    validation_data=load_data(filepath)
    return validation_data

def execute_experiment(config,organizations,validation_data,option):
    sample_validation_data_keys = random.sample(list(validation_data.keys()), 100)
    organization_results={}
    for organization_name in organizations.keys():
        experiments_results = {}
        if option==0:
            engine = RelevanceMetricEngine(config, organizations[organization_name], )
        elif option==1:
            engine = ActionabilityMetricEngine(config, organizations[organization_name])
        else:
            print("Need to select an option. 0: Relevance Metric, 1: Actionability Metric")
            break
        for sample_cti_key in sample_validation_data_keys:
            sample_cti = validation_data[sample_cti_key]
            experiments_results[sample_cti_key]=get_metric_experiment(engine,sample_cti)
        organization_results[organization_name]=experiments_results
    return organization_results

def relevance_metric_experiment(config,organization,sample_cti):
    engine = RelevanceMetricEngine(config, organization, sample_cti)
    return engine.get_metric()


def run_relevance_metric_experiments(config,validation_data):
    organizations_names, organizations_conf = prepare_relevance_metric_config()
    print("Loading the relevance metric organizations ..... ")
    organizations = {}
    for organization_name in organizations_names:
        organization = OrganizationRelevance(name=organization_name, config=config,
                                             params=organizations_conf[organization_name], load_from_file=True)
        organizations[organization_name] = organization
    experiment_results=execute_experiment(config,organizations,validation_data,0)
    return experiment_results


def get_metric_experiment(engine,sample_cti):
    engine.set_cti_product(sample_cti)
    return engine.get_metric()

def run_actionability_metric_experiments(config,validation_data):
    organizations_names, organizations_conf = prepare_actionability_metric_config()
    print("Loading the actionability metric organizations ..... ")
    organizations = {}
    for organization_name in organizations_names:
        organization = OrganizationActionability(name=organization_name, config=config,
                                             params=organizations_conf[organization_name], load_from_file=True)
        organizations[organization_name] = organization
    experiment_results=execute_experiment(config,organizations,validation_data,1)
    return experiment_results

def run_statistics(config):
    rel_metric_data=load_data(config['rel_results_path'])
    act_metric_results=load_data(config['act_results_path'])
    r_org_mean_values, r_org_values_per_landscape, r_org_cti_products_mean_values, r_org_cti_products_values_per_landscape=prepare_data_rel(rel_metric_data)
    a_org_mean_values, a_org_values_per_defence_mechanism, a_org_cti_products_mean_values, a_org_cti_products_values_per_landscape=prepare_data_act(act_metric_results)
    filename_rel_metric_comparison = os.path.join(config['plots_path'], 'products_rel_comparison.png')
    plot_products_metric_comparison(r_org_cti_products_mean_values,metric="Relevance",min_value=0.002,filename=filename_rel_metric_comparison)
    filename_act_metric_comparison = os.path.join(config['plots_path'], 'products_act_metric_comparison.png')
    plot_products_metric_comparison(a_org_cti_products_mean_values,metric="Actionability",min_value=0.005,filename=filename_act_metric_comparison)
    filename_violin_rel= os.path.join(config['plots_path'],'violin_plot_distributions_rel.png')
    plot_distributions_violin(r_org_cti_products_mean_values,"Relevance",min_value=0.0001,filename=filename_violin_rel)
    filename_violin_act = os.path.join(config['plots_path'], 'violin_plot_distributions_act.png')
    plot_distributions_violin(a_org_cti_products_mean_values, "Actionability", min_value=0.0001,size=1,filename=filename_violin_act,title="")
    filename_bar_rel= os.path.join(config['plots_path'], 'bar_plot_distributions_rel.png')
    plot_bar_distribution(r_org_cti_products_values_per_landscape,"Relevance",min_value=0.002,filename=filename_bar_rel,frame_type=2)
    filename_bar_act= os.path.join(config['plots_path'], 'bar_plot_distributions_act.png')
    plot_bar_distribution(a_org_cti_products_values_per_landscape,"Actionability",min_value=0.1,filename=filename_bar_act,frame_type=2)


def run():
    config = read_config("config/config.ini")
    print(f"Starting the experiment...")
    print("Loading validation data...")
    #validation_data = load_validation_data(config)
    print("Starting relevance metric experiments...")
    #rel_results=run_relevance_metric_experiments(config,validation_data)
    print(f"Writing relevance experiment results to file...{config['rel_results_path']}")
    #write_data(config['rel_results_path'],rel_results)
    print("Ending relevance metric experiments...")
    print("Starting actionability metric experiments...")
    #act_results=run_actionability_metric_experiments(config,validation_data)
    print(f"Writing relevance experiment results to file...{config['act_results_path']}")
    #write_data(config['act_results_path'], act_results)
    print("Ending actionability metric experiments...")
    print("Starting statistics calculations...")
    run_statistics(config)
    print("Ending statistics calculations...")
    print(f"End of the experiment.")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    run()
