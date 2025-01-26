"""
<Cyber Threat Intelligence Relevance and Actionability Quality Metrics Implementation.>
    Copyright (C) 2025  Georgios Sakellariou

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
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
