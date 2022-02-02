import pandas as pd

import re  # regular expression

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="ORGA-PINESS",
    description="A simple API to help you fix data related to your organization",
    version="0.1",
)

class Oragnisation(BaseModel):
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

# curl -d '{"bce": "BE0123.012.345", "name": "Trigu", "address": "Rue Ernest Bosh 6", "postal_code": "4123"}' -H "Content-Type: application/json" -s -X POST http://127.0.0.1:8002/orga_bce/ | jq
@app.post("/orga_bce/")
def output_address(data: Oragnisation):
    """
    A simple function that receive a bce number and output the address.
    :param review:
    :return: address, probabilities
    """

    return {
        "organisation": data
    }

# curl -d '{"bce": "BE0123.012.345", "name": "Trigu", "address": "Rue Ernest Bosh 6", "postal_code": "4123"}' -H "Content-Type: application/json" -s -X POST http://127.0.0.1:8002/orga_localisation/ | jq
@app.post("/orga_localisation/")
def output_bce(data: Oragnisation):
    """
    A simple function that receive an address, a postal code and a denomination and output the BCE with a probablilty.
    :param review:
    :return: address, probabilities
    """

    return {
        "organisation": data,
        "probabilities": '99.99%'
     }
     


