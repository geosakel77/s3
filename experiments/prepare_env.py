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

import json
from experiments.experiments_relevance_metric.prepare_relevance_metric_env import prepare_relevance_metric_env
from experiments.experiments_actionability_metric.prepare_actionability_metric_env import prepare_actionability_metric_env
from config.config import read_config
from s3lib.s3clientslib import LocalCTIClient
import random


def prepare_cti_data(config):
    print("Preparing CTI data.")
    cti_client = LocalCTIClient(config)

def prepare_validation_data(config):
    print("Preparing validation data...")
    filepath = config['validation_dataset']
    number = int(config['validation_data_number'])
    open_cti_client = LocalCTIClient(config, raw_data_client=False)
    keys = open_cti_client.cti_data.keys()
    validation_keys = random.sample(sorted(keys), number)
    validation_data ={}
    for key in validation_keys:
        validation_data[key] = open_cti_client.cti_data[key]
    print("Writing validation data to file...")
    with open(filepath, 'w') as f:
        json_object = json.dumps(validation_data, indent=4)
        f.write(json_object)
    print("Validation data prepared.")


def run():
    print(f"Starting the  experimental environment preparation...")
    config = read_config(filepath="../config/config.ini")
    prepare_relevance_metric_env(config)
    prepare_cti_data(config)
    prepare_validation_data(config)
    prepare_actionability_metric_env(config)
    print(f"Experimental environment preparation complete.")

if __name__ == '__main__':
    run()