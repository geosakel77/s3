from http.client import responses

from stix2validator.v21.musts import process

from config import read_config
from s3lib.libclients import OpenCTIClient, OpenAIClient, OntologyFIBOClient, CompaniesClient, OntologyNACEClient

CONFIG = read_config()


def run():
    CONFIG = read_config()
    #client = OpenCTIClient(CONFIG['api_url'], CONFIG['api_key'])
    #print(client.get_malware())
    #ontoclient = OntologyFIBOClient(CONFIG)
    #print(ontoclient.get_individuals())
    #openai_client =   OpenAIClient()
    #message="Give me an example of a business plan."
    #response= openai_client.call_openai(message)
    #print(response)
    #print(type(response))
    #companies_client = CompaniesClient(CONFIG)
    #print(companies_client.get_company(0))
    #print("--------------------")
    # #print(companies_client.get_companies_sample(5))
    #naceclient = OntologyNACEClient(CONFIG)
    #print(naceclient.loadeddata.data)





# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    run()
