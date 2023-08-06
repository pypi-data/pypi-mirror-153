import requests


base_url = "https://tx.fhir.org/r4/ValueSet/$expand?url="
headers = {"accept": "application/json"}

def expand_value_set(value_set_url: str) -> dict:
    r = requests.get(base_url + value_set_url, headers=headers)
    value_set_resource = r.json()
    value_set_contents = value_set_resource["expansion"]["contains"]
    for value in value_set_contents:
        del value["extension"]
    return value_set_contents
