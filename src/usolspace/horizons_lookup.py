import requests

BASE = "https://ssd-api.jpl.nasa.gov/api/horizons_lookup.api"


def lookup(search: str, timeout: int = 60):
    params = {"format": "json", "COMMAND": search}
    r = requests.get(BASE, params=params, timeout=timeout)
    r.raise_for_status()
    return r.json()
