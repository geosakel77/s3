from unittest import TestCase
from config import read_config


class Test(TestCase):

    def setUp(self):
        self.config = read_config(filepath="../config.ini")

    def test_read_config(self):
        list_of_keys = ['openai_model', 'debug_mode', 'log_level', 'api_url', 'api_key', 'openai_api_key',
                        'openai_organization_id', 'openai_project_id', 'fibo_path', 'fibo_entry', 'dit_entry',
                        'nace_path', 'dit_path', 'nace_entry','skos_entry','dcat_entry']

        self.assertCountEqual(self.config.keys(), list_of_keys, "Configuration Keys Exist")
