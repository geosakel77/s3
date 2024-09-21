from http.client import responses

from stix2validator.v21.musts import process

from config import read_config
from s3lib import OpenCTIClient, OpenAIClient,OntologyFIBOClient
CONFIG = read_config()


def run():
    CONFIG = read_config()
    #client = OpenCTIClient(CONFIG['api_url'], CONFIG['api_key'])
    #print(client.get_malware())
    ontoclient = OntologyFIBOClient(CONFIG)
    print(ontoclient.get_individuals())
    #openai_client =   OpenAIClient()
    #message="Give me an example of a business plan."
    #response= openai_client.call_openai(message)
    #print(response)
    #print(type(response))



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    run()
