import requests
import pandas as pd
import re  # regular expression
import unicodedata
from slugify import slugify
import time
from bs4 import BeautifulSoup

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="ORGA-PINESS",
    description="A simple API to help you fix data related to your organisation",
    version="0.1",
)

class Organisation(BaseModel):
    bce: str = None
    name: str = None
    address: str = None
    postal_code: str = None


@app.get("/")
def read_root():
    return {
        "msg": "Welcome to the ORG-APINESS",
        "docs": 'http://localhost:8002/docs/'
    }

@app.get("/status")
def read_status():
        return {"msg": "The API is running"}

# curl -s -X 'POST' \
#   'http://localhost:8002/find_organisation/' \
#   -H 'accept: application/json' \
#   -H 'Content-Type: application/json' \
#   -d '{
#   "bce": "BE0123456789",
#   "name": "Trigu",
#   "address": "Rue de la Gare, 10",
#   "postal_code": "1000"
# }' | jq
@app.post("/find_organisation/") 

async def output(data: Organisation):
    """
    A simple function that receive an organisation and output the info based on what it found online.
    : return complementary info and fiability of the prediction
    """
    start_time = time.time()

    if data.bce is not None and data.bce != "":
        return find_address(data)
    else:
        return find_bce(data)
    
def find_bce(data):
    start_time = time.time()

    url = "https://kbopub.economie.fgov.be/kbopub/zoeknaamfonetischform.html?searchWord=" + name + "&_oudeBenaming=on&pstcdeNPRP=&postgemeente1=&ondNP=true&_ondNP=on&ondRP=true&_ondRP=on&rechtsvormFonetic=ALL&vest=true&_vest=on&filterEnkelActieve=true&_filterEnkelActieve=on&actionNPRP=Rechercher"

    return {
        "meta": {   
            "status": "success",
            "duration_in_seconds": time.time() - start_time
        },
        "msg": "The BCE is missing",
        "organisation": data,
        "fiability": '99.99%'
    }

def find_address(data):
    start_time = time.time()
  
    company_number = data.bce
    
    # https://kbopub.economie.fgov.be/kbopub/zoeknummerform.html?nummer=0685595109

    url = "https://kbopub.economie.fgov.be/kbopub/zoeknummerform.html?nummer=" + company_number

    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    tds = soup.find_all('td', class_='RL')

    for td in tds:
        # if td contain link with alt text of Stratenplan
        if td.find('img', alt='Stratenplan'):
            # remove useless span
            td.find('span').decompose()
            # get the address
            address = td.get_text()

    data.address = address
    

    return {
        "meta": {   
            "status": "success",
            "duration_in_seconds": time.time() - start_time
        },
        "msg": "The BCE is present",
        "organisation": data,
        "fiability": '99.99%'
    }
        
