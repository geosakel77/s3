from unittest import TestCase

from config.config import read_config


class Test(TestCase):

    def setUp(self):
        self.config = read_config(filepath="../config/config.ini")

    def test_read_config(self):
        list_of_keys = ['openai_model', 'debug_mode', 'log_level', 'api_url', 'api_key', 'openai_api_key',
                        'openai_organization_id', 'openai_project_id', 'fibo_path', 'fibo_entry_loans',
                        'fibo_entry_funds', 'fibo_entry_fps',
                        'nace_path', 'nace_entry', 'skos_entry', 'dcat_entry', 'companies_path',
                        'nace_json', 'gpo_path', 'gpo_entry', 'cpe_path', 'eccf_path', 'eccf_entry', 'pto_path',
                        'pto_entry', 'pto_json', 'rc1', 'rc2', 'rc3', 'rc4', 'rc5', 'rc6', 'rc7', 'rc8', 'rc9', 'rc10',
                        'landscape_lo', 'landscape_li', 'landscape_ltp', 'industries_choice',
                        'business_activities_choice', 'ac1', 'ac2', 'ac3', 'ac4', 'ac5', 'ac6', 'ac7', 'ac8', 'ac9',
                        'ac10']

        self.assertCountEqual(self.config.keys(), list_of_keys, "Configuration Keys Exist")
