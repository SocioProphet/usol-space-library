import requests

LOOKUP = "https://ssd-api.jpl.nasa.gov/sbdb.api"
QUERY = "https://ssd-api.jpl.nasa.gov/sbdb_query.api"
CAD = "https://ssd-api.jpl.nasa.gov/cad.api"


def lookup(sstr: str, fields: str = None, timeout: int = 60):
    params = {"sstr": sstr}
    if fields:
        params["fields"] = fields
    r = requests.get(LOOKUP, params=params, timeout=timeout)
    r.raise_for_status()
    return r.json()


def query(**filters):
    r = requests.get(QUERY, params=filters, timeout=60)
    r.raise_for_status()
    return r.json()


def cad(**filters):
    r = requests.get(CAD, params=filters, timeout=60)
    r.raise_for_status()
    return r.json()
