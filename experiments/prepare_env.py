
import os
import multiprocessing
from multiprocessing import Process,Pool

from openai import organization


from config.config import read_config
from config.orgprofilesconf import *
from s3lib.s3organizationslib import OrganizationRelevance

def create_organization(name,config,parameters):
    organization = OrganizationRelevance(name,config,parameters)
    return organization

def run():
    print(f"Starting the experimental environment preparation...")
    print("Reading the experimental environment configuration...")
    CONFIG = read_config("../config/config.ini")
    print(f"Reading the organizations configuration files...")
    organizations_names = ['c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'c10']
    organizations_conf = {'c1':C1,'c2':C2,'c3':C3, 'c4':C4, 'c5':C5, 'c6':C6, 'c7':C7, 'c8':C8, 'c9':C9, 'c10':C10}
    items = []
    for organization_name in organizations_names:
        items.append((organization_name,CONFIG,organizations_conf[organization_name]))
    try:
        with multiprocessing.Pool(processes=2,maxtasksperchild=6) as pool:
            for result in pool.starmap(create_organization, items):
                print(result)
    except Exception as e:
        print(e)

    print(f"End of the experimental environment preparation")

if __name__ == '__main__':
    run()