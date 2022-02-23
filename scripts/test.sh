#!/bin/sh

set -e

# CURRENT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
# BASE_DIR="$(dirname "$CURRENT_DIR")"

# pytest "${BASE_DIR}/tests" "$*"

# coverage run --rcfile "${BASE_DIR}/pyproject.toml" -m pytest "${BASE_DIR}/tests" "$*"
# coverage html --rcfile "${BASE_DIR}/pyproject.toml"

echo "-------------"
echo "with company number with wrong address";
echo "-------------"

curl -s -X 'POST' \
  'http://localhost:8002/find_organisation' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "company_number": "0685595109",
  "name": "Mesylab",
  "address": "Rue Robespierre, 10",
  "postal_code": "41000",
  "city": "Sprimont"
}' | jq


echo "-------------"
echo "with company number, correct address, but not active";
echo "-------------"

curl -s -X 'POST' \
  'http://localhost:8002/find_organisation' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "company_number": "BE0653-970.139",
  "name": "TagData",
  "address": "Rue de la chaine, 6",
  "postal_code": "4000"
}' | jq


echo "-------------"
echo "with WRONG company number";
echo "-------------"


curl -s -X 'POST' \
  'http://localhost:8002/find_organisation' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "company_number": "BE0652-970.139",
  "name": "Mesylab",
  "address": "Rue Robespierre, 6",
  "postal_code": "4000"
}' | jq


echo "-------------"
echo "without company number";
echo "-------------"


curl -s -X 'POST' \
  'http://localhost:8002/find_organisation' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "company_number": "",
  "name": "Mesylab",
  "address": "Rue Robespierre, 6",
  "postal_code": "4140"
}' | jq