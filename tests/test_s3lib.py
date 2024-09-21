from unittest import TestCase
from s3lib import OpenAIClient, OpenCTIClient
from config import read_config


CONFIG= read_config('../config.ini')


class TestOpenCTIClient(TestCase):
    def setUp(self):
        self.client = OpenCTIClient(CONFIG['api_url'], CONFIG['api_key'])

    def test_get_malware(self):
        response=self.client.get_malware()
        self.assertGreater(len(response),10)


class TestOpenAIClient(TestCase):
    def setUp(self):
        self.client = OpenAIClient(config=CONFIG)

    def test_call_openai(self):
        response = self.client.call_openai("Give an example of LLM")
        self.assertGreater(len(response),10)

