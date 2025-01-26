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

import nltk

class Engine:
    def __init__(self,config,organization,product):
        self.config = config
        self.organization = organization
        self.product = product
        self.engine_core =None

    def get_metric(self):
        pass

    def set_cti_product(self,cti_product):
        self.product = cti_product

class EngineCore:
    def __init__(self,config,product):
        self.config = config
        self.product = product
        nltk.download('stopwords')
        nltk.download('wordnet')

    def calculate_metric(self):
        pass

