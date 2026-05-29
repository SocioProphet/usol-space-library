import requests
from typing import Dict, Any

BASE = "https://ssd-api.jpl.nasa.gov/api/horizons.api"


def ephemeris(
    command: str,
    center: str,
    start_time: str,
    stop_time: str,
    step_size: str,
    quantities: str = "1,9,20",
    obj_data: str = "NO",
    ephem_type: str = "OBSERVER",
    make_ephem: str = "YES",
    timeout: int = 60,
) -> Dict[str, Any]:
    params = {
        "format": "json",
        "COMMAND": command,
        "OBJ_DATA": obj_data,
        "MAKE_EPHEM": make_ephem,
        "EPHEM_TYPE": ephem_type,
        "CENTER": center,
        "START_TIME": start_time,
        "STOP_TIME": stop_time,
        "STEP_SIZE": step_size,
        "QUANTITIES": quantities,
    }
    r = requests.get(BASE, params=params, timeout=timeout)
    r.raise_for_status()
    return r.json()
