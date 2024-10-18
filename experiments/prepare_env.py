from s3lib.relevance.s3landscapeslib import InputLandscape,TransformationProcessLandscape
from config.config import read_config
from config.orgprofilesconf import C1
def run():
    print(f"Starting  ")

    CONFIG = read_config("../config/config.ini")
    #landscape_li=InputLandscape(config=CONFIG,params=C1)
    landscape_tp=TransformationProcessLandscape(CONFIG,params=C1)

if __name__ == '__main__':
    run()