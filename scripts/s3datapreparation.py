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

from s3lib.s3clientslib import OntologyNACEClient,OntologyPTOClient,MandiantCTIClient,OpenCTIClient

def data_rel_preparation(config):
    """
    Prepares and writes NACE and PTO data using the specified configuration.

    This function performs the following steps:
    1. Initializes NACE and PTO clients with the provided configuration.
    2. Fetches NACE data and writes it to a file.
    3. Fetches PTO data and writes it to a file.

    Parameters:
    config (dict): Configuration settings required by NACE and PTO clients.

    Returns:
    None
    """
    print("Starting Data Preparation...")
    print("Preparing NACE Data...")
    nace_client = OntologyNACEClient(config)
    nace_client.get_data()
    nace_client.write_to_file()
    print("Data Preparation Complete")
    print("Preparing PTO Data...")
    pto_client = OntologyPTOClient(config)
    pto_client.get_data()
    pto_client.write_to_file()
    print("Data Preparation Complete")

def data_act_preparation(config):
    print("Starting Data Preparation...")
    print("Preparing Reports Data...")
    client= MandiantCTIClient(config,epoch=14)
    client.write_reports()
    client = OpenCTIClient(config=config, number_of_reports=30000)
    print("Data Preparation Complete")