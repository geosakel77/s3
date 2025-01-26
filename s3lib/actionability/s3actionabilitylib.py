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

from s3lib.s3engineslib import Engine, EngineCore
from probables import CuckooFilter
from statistics import mean

class ActionabilityMetricEngine(Engine):

    def __init__(self,config,target_organization=None, cti_product=None,capacity = 1000,bucket_size = 4,max_swaps = 10,auto_expand=True,finger_size=2 ):
        super().__init__(config,target_organization,cti_product)
        self.capacity = capacity
        self.bucket_size = bucket_size
        self.max_swaps = max_swaps
        self.auto_expand = auto_expand
        self.finger_size = finger_size
        self._create_cuckoo_filters()
        #self.engine_core= self.ActionabilityMetricCore(self.config,self.product,self.cuckoo_filters)


    def _create_cuckoo_filters(self):
        self.cuckoo_filters={}
        for key in self.organization.defence_mechanisms.keys():
            self.cuckoo_filters[key]=self._create_cuckoo_filter(self.organization.defence_mechanisms[key].knowledge_base)


    def _create_cuckoo_filter(self,knowledge_base):
        cuckoo_filter = CuckooFilter(capacity=self.capacity, bucket_size=self.bucket_size, max_swaps=self.max_swaps,auto_expand=self.auto_expand,finger_size=self.finger_size)
        for key in knowledge_base.keys():
            for item in knowledge_base[key]:
                cuckoo_filter.add(item)
        print(f"Created cuckoo filter  with load: {cuckoo_filter.load_factor()}")
        return cuckoo_filter


    def get_metric(self):
        self.engine_core = self.ActionabilityMetricCore(self.config, self.product, self.cuckoo_filters)
        return self.engine_core.calculate_metric()

    class ActionabilityMetricCore(EngineCore):

        def __init__(self,config,cti_product,cuckoo_filters):
            super().__init__(config,cti_product)
            self.cuckoo_filters=cuckoo_filters

        def calculate_metric(self):
            results={}
            for key in self.cuckoo_filters.keys():
                results[key]=[]
                t_r=0
                f_r=0
                for item in self.product:
                    if self.cuckoo_filters[key].check(item):
                        t_r+=1
                    else:
                        f_r+=1
                results[key].append(t_r/(t_r+f_r))
            pos_results_list=[]
            for key in results.keys():
                pos_results_list.append(results[key][0])
            return [mean(pos_results_list),pos_results_list]