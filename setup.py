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


from config.config import read_config
from scripts.s3datapreparation import data_rel_preparation,data_act_preparation
from scripts.s3prepareorganizations import prepare_rel_organizations, prepare_act_organizations


def run_relevance_metric_setup():
    config = read_config('config/config.ini')
    print("Preparing relevance organizations configuration files...")
    prepare_rel_organizations(config)
    print("Organizations' configuration has been prepared.")
    print("Preparing datasets...")
    data_rel_preparation(config)
    print("Datasets has been prepared.")

def run_actionability_metric_setup():
    config = read_config('config/config.ini')
    print("Preparing actionability organizations configuration files...")
    prepare_act_organizations(config)
    print("Organizations' configuration has been prepared.")
    print("Preparing datasets...")
    data_act_preparation(config)
    print("Datasets has been prepared.")


if __name__ == '__main__':
    run_relevance_metric_setup()
    run_actionability_metric_setup()