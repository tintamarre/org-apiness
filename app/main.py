import requests
import pandas as pd
import re  # regular expression
import unicodedata

# from slugify import slugify
import time
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="ORGA-PINESS",
    description="A simple API to help you fix data related to your organisation",
    version="0.1",
)

class Organisation(BaseModel):
    company_number: str = ""
    name: str = ""
    address: str = ""
    postal_code: str = ""
    city: str = ""


class Ratio(BaseModel):
    name: int = 0
    address: int = 0
    postal_code: int = 0
    city: int = 0


@app.get("/")
async def read_root():
    return {
        "msg": "Welcome to the ORG-APINESS",
        "docs": "http://localhost:8002/docs/",
        "license": "GNU General Public License v3.0",
        "credits": "Fédération Wallonie-Bruxelles",
        "links": [
            {
                "name": "Find organisation",
                "type": "POST",
                "url": "http://localhost:8002/find_organisation",
            },
            {"name": "Status", "type": "GET", "url": "http://localhost:8002/status"},
        ],
    }


@app.get("/status")
async def read_status():
    return {"msg": "The API is running"}


# curl -s -X 'POST' \
#   'http://localhost:8002/find_organisation/' \
#   -H 'accept: application/json' \
#   -H 'Content-Type: application/json' \
#   -d '{
#   "company_number": "BE0123456789",
#   "name": "Trigu",
#   "address": "Rue de la Gare, 10",
#   "postal_code": "1000"
# }' | jq
@app.post("/find_organisation")
async def output(data: Organisation):
    """
    A simple function that receive an organisation, find the organisation in the public repository and output the complementary info and comparaison ratio
    """

    if data.company_number is not None and data.company_number != "":
        # We have a company_number
        return find_address(time.time(), data)
    else:
        if data.name is not None and data.name != "":
            # We have a name
            return find_company_number(time.time(), data)
        else:
            return {
                "meta": {
                    "status": "error",
                    "duration_in_seconds": time.time() - start_time
                    }, 
            "msg": "The company_number or the name is missing"
            }            

def find_company_number(start_time, data):

    url = (
        "https://kbopub.economie.fgov.be/kbopub/zoeknaamfonetischform.html?searchWord="
        + data.name
        + "&_oudeBenaming=on&pstcdeNPRP=&postgemeente1=&ondNP=true&_ondNP=on&ondRP=true&_ondRP=on&rechtsvormFonetic=ALL&vest=true&_vest=on&filterEnkelActieve=true&_filterEnkelActieve=on&actionNPRP=Rechercher"
    )

    soup = get_request(url)

    return {
        "meta": {"status": "success", "duration_in_seconds": time.time() - start_time},
        "msg": "The company_number is missing",
        "organisation": data,
        "url": url,
        "fiability": "100%",
    }


def find_address(start_time, data):
    # start_time = time.time()
    global new_name, full_address, new_address, new_postal_code, new_city

    # reset the global variables
    new_name = ""
    full_address = ""
    new_address = ""
    new_postal_code = ""
    new_city = ""

    data.company_number = re.sub("[^0-9]", "", data.company_number)

    company_number = data.company_number

    url = (
        "https://kbopub.economie.fgov.be/kbopub/zoeknummerform.html?lang=en&nummer="
        + company_number
    )
    # url = "https://statuts.notaire.be/costa_v1/enterprises/" + company_number
    # url = "https://statuts.notaire.be/costa_v1/api/enterprise-api/enterprises/" + company_number

    soup = get_request(url)

    # if nothing found return error
    if soup.select("span#nummer.error") is not None:
        return {
            "meta": {"status": "error", "duration_in_seconds": time.time() - start_time},
            "msg": "No organisation found",
            "organisation": data,
            "url": url,
            "fiability": "100",
        }

    tds = soup.find_all("td", class_="QL")
    for td in tds:
        if td.text.strip() == "Name:":

            # remove the span tag
            new_name = td.find_next_sibling('td').text.strip()
            break

    tds = soup.find_all("td", class_="RL")
    for td in tds:
        # if td contain link with alt text of Stratenplan
        if td.find("img", alt="Map"):
            # remove useless span
            td.find("span").decompose()
            # get the address
            full_address = td.get_text().strip()
            full_address = full_address.split("\n")

            new_address = full_address[0].strip()
            new_postal_code = full_address[1].strip()[:4].strip()
            new_city = full_address[1].strip()[4:].strip()

            # postal_code = full_address.split(',')[1]
            # city = full_address.split(',')[2]

    # define new organisation
    new_organisation = Organisation(
        company_number=company_number,
        name=new_name,
        address=new_address,
        postal_code=new_postal_code,
        city=new_city,
    )

    # compare new_organisation with data and return the ratio of similarity
    ratios = Ratio(
        name=fuzz.ratio(new_organisation.name.lower(), data.name.lower()),
        address=fuzz.ratio(new_organisation.address.lower(), data.address.lower()),
        postal_code=fuzz.ratio(new_organisation.postal_code, data.postal_code),
        city=fuzz.ratio(new_organisation.city.lower(), data.city.lower()),
    )

    # return the average of the ratio of similarity
    average_of_similarity = (
        ratios.name + ratios.address + ratios.postal_code + ratios.city
    ) / 4

    return {
        "meta": {"status": "success", "duration_in_seconds": time.time() - start_time},
        "msg": "The company_number is present",
        "url": url,
        "organisation": data,
        "new_organisation": new_organisation,
        "ratios": ratios,
        "ratios_avg": average_of_similarity,
    }

    # RAISE EXCEPTION IF NO DATA FOUND
    raise HTTPException(status_code=404, detail="No data found")


def get_request(url):
    page = requests.get(url)

    # if request failed
    if page.status_code != 200:
        return {"msg": "The request failed"}
    else:
        soup = BeautifulSoup(page.text, "html.parser")
        return soup
