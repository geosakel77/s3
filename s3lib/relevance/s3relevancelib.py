import json

from s3lib.s3engineslib import Engine, EngineCore
from datasketch import MinHash
from statistics import mean
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


class RelevanceMetricEngine(Engine):

    def __init__(self,config,target_organization=None, cti_product=None):
        super().__init__(config,target_organization,cti_product)
        self.engine_core=self.RelevanceMetricCore(self.config,self.organization,self.product)

    def _set_organization(self,target_organization):
        self.organization = target_organization

    def _set_product(self,cti_product):
        self.product = cti_product

    def get_metric(self):
        return self.engine_core.calculate_metric()


    class RelevanceMetricCore(EngineCore):
        def __init__(self,config,target_organization, cti_product):
            super().__init__(config,target_organization,cti_product)

        def calculate_metric(self):
            return mean([self.calculate_output_landscape_minhash(),self.calculate_input_landscape_minhash(),self.calculate_transformation_process_landscape()])

        def calculate_input_landscape_minhash(self):
            input_landscape = self.organization.input_landscape
            suppliers=self._clean_suppliers(input_landscape.suppliers)
            #print(suppliers)
            loans=self._clean_loans(input_landscape.loans)
            print(loans)
            #print(input_landscape.funds)
            #print(input_landscape.loans)


            #TODO
            return 1
        def _clean_loans(self,loans):
            cleaned_loans=[]
            text_loans=""
            for loan in loans:
                loan_split=loan.split('```')
                for loan_split_part in loan_split:
                    if loan_split_part.startswith('json'):
                        data = self._clean_dict(loan_split_part.replace("json",""))
                        text_loans += data
                    elif 'threats' in loan_split_part.lower():
                        text_loans += loan_split_part
            cleaned_loans.extend(self._clean_text(text_loans))
            return cleaned_loans


        def _clean_suppliers(self,suppliers):
            cleaned_suppliers=""
            for key in suppliers.keys():
                supplier=suppliers[key]
                doc_supplier=""
                for info_part in supplier:
                    doc_supplier+=info_part
                cleaned_suppliers+=doc_supplier
            return self._clean_text(cleaned_suppliers)

        def calculate_output_landscape_minhash(self):
            return 1

        def calculate_transformation_process_landscape(self):
            return 1

        def _clean_text(self,text_to_clean):
            text_data=text_to_clean
            text_data=text_data.lower()
            text_data = text_data.split()
            wl = WordNetLemmatizer()
            text_data=[wl.lemmatize(word) for word in text_data if not word in set(stopwords.words('english'))]
            text_data=[re.sub('[^A-Za-z0-9.-]+','',word) for word in text_data if len(word)>2]
            cleaned_text_words=[]
            for word in text_data:
                if word.endswith('.'):
                    text= word
                    word=text[:text.rfind('.')] + text[text.rfind('.') + 1:]
                    cleaned_text_words.append(word)
                else:
                    cleaned_text_words.append(word)
            text_data=cleaned_text_words
            text_data=set(text_data)
            return text_data

        def _clean_dict(self,dict_data):
            text_data=dict_data
            text_data=text_data.lower().replace('}','').replace('{','').replace('"','').replace('_',' ').replace('\n',' ').replace('\t',' ').replace(':','').replace(',','')
            return text_data