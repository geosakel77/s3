import random,json,math


def prepare_rel_organizations(config):
    organizations = ['c1','c2','c3','c4','c5','c6','c7','c8','c9','c10']
    path_to_write= "config/orgrelprofilesconf.py"

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

def prepare_act_organizations(config):
    organizations = ['c1','c2','c3','c4','c5','c6','c7','c8','c9','c10']
    path_to_write= "config/orgactprofilesconf.py"

    with open(path_to_write,"w+") as f:
        f.write("")
    for organization in organizations:
        k_sets=random.randint(3,30)
        cti_products_number=random.randint(300,1000)
        products_per_k_set=int(cti_products_number/k_sets)
        products_per_k_set=math.floor(products_per_k_set)
        cti_products_number=products_per_k_set*k_sets
        org_config = {'k_sets': k_sets,'cti_products_number':cti_products_number,'products_per_k_set':products_per_k_set}
        data_to_write = f"{organization.capitalize()}={json.dumps(org_config)}\n"
        with open(path_to_write, "a") as f:
            f.write(data_to_write)