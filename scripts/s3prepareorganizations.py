import random,json


def prepare_organizations(CONFIG):
    organizations = ['c1','c2','c3','c4','c5','c6','c7','c8','c9','c10']
    path_to_write= "config/orgprofilesconf.py"

    with open(path_to_write,"w+") as f:
        f.write("")

    for organization in organizations:
        org_config = {'competitors_size': random.randint(5, 20), 'competitors_industries': random.randint(2, 10),
                      'suppliers_size': random.randint(5, 20), 'suppliers_industries': random.randint(2, 10),
                      'number_of_cs_loans': random.randint(0, 8), 'number_of_cs_funds': random.randint(0, 8),
                      'business_activities_choice': random.randint(2, 15),
                      'business_activities_size': random.randint(5, 15),
                      'number_of_internal_operations': random.randint(1, 10),
                      'number_of_information_systems': random.randint(10, 20),
                      'number_of_products': random.randint(1, 10), 'number_of_services': random.randint(1, 10)}
        data_to_write = f"{organization.capitalize()}={json.dumps(org_config)}\n"
        with open(path_to_write, "a") as f:
            f.write(data_to_write)