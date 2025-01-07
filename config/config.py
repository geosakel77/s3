import configparser

import configparser
from config.industries import INDUSTRIES
from config.business_activities import BUSINESS_ACTIVITIES
import config.orgrelprofilesconf as rel_org_conf
import config.orgactprofilesconf as act_org_conf

def prepare_relevance_metric_config():
    print(f"Reading the relevance metric organizations configuration files...")
    organizations_names = ['rc1', 'rc2', 'rc3', 'rc4', 'rc5', 'rc6', 'rc7', 'rc8', 'rc9', 'rc10']
    organizations_conf = {'rc1': rel_org_conf.C1, 'rc2': rel_org_conf.C2, 'rc3': rel_org_conf.C3, 'rc4': rel_org_conf.C4,
                          'rc5': rel_org_conf.C5, 'rc6': rel_org_conf.C6, 'rc7': rel_org_conf.C7, 'rc8': rel_org_conf.C8,
                          'rc9': rel_org_conf.C9,
                          'rc10': rel_org_conf.C10}
    return organizations_names, organizations_conf


def prepare_actionability_metric_config():
    print(f"Reading the actionability metric organizations configuration files...")
    organizations_names = ['ac1', 'ac2', 'ac3', 'ac4', 'ac5', 'ac6', 'ac7', 'ac8', 'ac9', 'ac10']
    organizations_conf = {'ac1': act_org_conf.C1, 'ac2': act_org_conf.C2, 'ac3': act_org_conf.C3, 'ac4': act_org_conf.C4,
                          'ac5': act_org_conf.C5, 'ac6': act_org_conf.C6, 'ac7': act_org_conf.C7, 'ac8': act_org_conf.C8,
                          'ac9': act_org_conf.C9,
                          'ac10': act_org_conf.C10}
    return organizations_names, organizations_conf

def read_config(filepath="config.ini"):
    # Create a ConfigParser object
    config = configparser.ConfigParser()

    # Read the configuration file
    config.read(filepath)

    # Access values from the configuration file
    debug_mode = config.getboolean('general', 'debug')
    font_path=config.get('general', 'font_path')
    log_level = config.get('general', 'log_level')
    api_url = config.get('opencti', 'api_url')
    api_key = config.get('opencti', 'api_key')
    mandiant_key_id = config.get('opencti', 'mandiant_key_id')
    mandiant_key_secret = config.get('opencti', 'mandiant_key_secret')
    reports_path = config.get('opencti', 'reports_path')
    cti_data_path =config.get('dataset', 'cti_data_path')
    images_path = config.get('opencti', 'images_path')
    openai_api_key = config.get('openai', 'openai_api_key')
    openai_organization_id = config.get('openai', 'organization_id')
    openai_project_id = config.get('openai', 'project_id')
    openai_model = config.get('openai', 'model')
    fibo_path = config.get('ontology', 'fibo_path')
    fibo_entry_funds = config.get('ontology', 'fibo_entry_funds')
    fibo_entry_fps = config.get('ontology', 'fibo_entry_fps')
    fibo_entry_loans = config.get('ontology', 'fibo_entry_loans')
    nace_path = config.get('ontology', 'nace_path')
    nace_entry = config.get('ontology', 'nace_entry')
    skos_entry = config.get('ontology', 'skos_entry')
    dcat_entry = config.get('ontology', 'dcat_entry')
    nace_json = config.get('ontology', 'nace_json')
    gpo_path = config.get('ontology', 'gpo_path')
    gpo_entry = config.get('ontology', 'gpo_entry')
    eccf_entry = config.get('ontology', 'eccf_entry')
    eccf_path = config.get('ontology', 'eccf_path')
    companies_entry = config.get('dataset', 'companies_path')
    cpe_path = config.get('dataset', 'cpe_path')
    pto_path = config.get('ontology', 'pto_path')
    pto_entry = config.get('ontology', 'pto_entry')
    pto_json = config.get('ontology', 'pto_json')
    rc1 = config.get('experiments', 'rc1')
    rc2 = config.get('experiments', 'rc2')
    rc3 = config.get('experiments', 'rc3')
    rc4 = config.get('experiments', 'rc4')
    rc5 = config.get('experiments', 'rc5')
    rc6 = config.get('experiments', 'rc6')
    rc7 = config.get('experiments', 'rc7')
    rc8 = config.get('experiments', 'rc8')
    rc9 = config.get('experiments', 'rc9')
    rc10 = config.get('experiments', 'rc10')
    landscape_lo = config.get('experiments', 'landscape_LO')
    landscape_li = config.get('experiments', 'landscape_LI')
    landscape_ltp = config.get('experiments', 'landscape_LTP')
    ac1 = config.get('experiments', 'ac1')
    ac2 = config.get('experiments', 'ac2')
    ac3 = config.get('experiments', 'ac3')
    ac4 = config.get('experiments', 'ac4')
    ac5 = config.get('experiments', 'ac5')
    ac6 = config.get('experiments', 'ac6')
    ac7 = config.get('experiments', 'ac7')
    ac8 = config.get('experiments', 'ac8')
    ac9 = config.get('experiments', 'ac9')
    ac10 = config.get('experiments', 'ac10')
    validation_dataset = config.get('experiments', 'validation_dataset')
    validation_data_number=config.get('experiments', 'validation_data_number')
    rel_results_path=config.get('results', 'rel_results_path')
    act_results_path=config.get('results', 'act_results_path')
    plots_path=config.get('results', 'plots_path')
    industries_choice = INDUSTRIES
    business_activities_choice = BUSINESS_ACTIVITIES
    # Return a dictionary with the retrieved values
    config_values = {
        'debug_mode': debug_mode,
        'font_path': font_path,
        'log_level': log_level,
        'api_url': api_url,
        'api_key': api_key,
        'cti_data_path': cti_data_path,
        'mandiant_key_id': mandiant_key_id,
        'mandiant_key_secret': mandiant_key_secret,
        'reports_path': reports_path,
        'images_path': images_path,
        'openai_api_key': openai_api_key,
        'openai_organization_id': openai_organization_id,
        'openai_project_id': openai_project_id,
        'openai_model': openai_model,
        'fibo_path': fibo_path,
        'fibo_entry_funds': fibo_entry_funds,
        'fibo_entry_fps': fibo_entry_fps,
        'fibo_entry_loans': fibo_entry_loans,
        'nace_path': nace_path,
        'nace_entry': nace_entry,
        'skos_entry': skos_entry,
        'dcat_entry': dcat_entry,
        'nace_json': nace_json,
        'companies_path': companies_entry,
        'gpo_path': gpo_path,
        'gpo_entry': gpo_entry,
        'cpe_path': cpe_path,
        'eccf_entry': eccf_entry,
        'eccf_path': eccf_path,
        'pto_path': pto_path,
        'pto_entry': pto_entry,
        'pto_json': pto_json,
        'rc1': rc1,
        'rc2': rc2,
        'rc3': rc3,
        'rc4': rc4,
        'rc5': rc5,
        'rc6': rc6,
        'rc7': rc7,
        'rc8': rc8,
        'rc9': rc9,
        'rc10': rc10,
        'landscape_lo': landscape_lo,
        'landscape_li': landscape_li,
        'landscape_ltp': landscape_ltp,
        'industries_choice': industries_choice,
        'business_activities_choice': business_activities_choice,
        'ac1': ac1,
        'ac2': ac2,
        'ac3': ac3,
        'ac4': ac4,
        'ac5': ac5,
        'ac6': ac6,
        'ac7': ac7,
        'ac8': ac8,
        'ac9': ac9,
        'ac10': ac10,
        'validation_dataset': validation_dataset,
        'validation_data_number': validation_data_number,
        'rel_results_path': rel_results_path,
        'act_results_path': act_results_path,
        'plots_path': plots_path
    }

    return config_values
