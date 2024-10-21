import os.path

from config.config import read_config
from config.orgprofilesconf import *



def run():
    print(f"Starting the experimental environment preparation...")
    print("Reading the experimental environment configuration...")
    CONFIG = read_config("../config/config.ini")
    print(f"Reading the organizations configuration files...")
    organizations_names = ['c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'c10']
    organizations_conf = {'c1':C1,'c2':C2,'c3':C3, 'c4':C4, 'c5':C5, 'c6':C6, 'c7':C7, 'c8':C8, 'c9':C9, 'c10':C10}
    print("Creating the organizations ..... ")
    for organization_name in organizations_names:
        print(f"Creating organization {organization_name}...")
        print(CONFIG[organization_name])

    print(f"Writing organizations to files...")
    for organization_name in organizations_names:
        print(f"Creating paths for {organization_name}...")
        organization_path= CONFIG[organization_name]
        print(organization_path)
        landscape_li_path = os.path.join(organization_path,CONFIG["landscape_li"])
        landscape_li_capital_sources_path= os.path.join(str(landscape_li_path),"capital_sources")
        landscape_li_competitors_path = os.path.join(str(landscape_li_path), "competitors")
        landscape_li_suppliers_path = os.path.join(str(landscape_li_path), "suppliers")
        landscape_lo_path = os.path.join(organization_path, CONFIG["landscape_lo"])
        landscape_lo_products_path = os.path.join(str(landscape_lo_path), "products")
        landscape_lo_competitors_path = os.path.join(str(landscape_lo_path), "services")
        landscape_ltp_path = os.path.join(organization_path, CONFIG["landscape_ltp"])
        landscape_ltp_business_activities_path = os.path.join(str(landscape_ltp_path), "business_activities")
        landscape_ltp_information_systems_path = os.path.join(str(landscape_ltp_path), "information_systems")
        landscape_ltp_internal_operations_path = os.path.join(str(landscape_ltp_path), "internal_operations")




    #landscape_li=InputLandscape(config=CONFIG,params=C1)
    #landscape_tp=OutputLandscape(CONFIG,params=C1)
    print(f"End of the experimental environment preparation")

if __name__ == '__main__':
    run()