import requests

BASE = "https://ssd-api.jpl.nasa.gov/sb_ident.api"


def identify(
    utc_time: str,
    ra: float,
    dec: float,
    fov_w: float,
    fov_h: float,
    site: str = "500@399",
    maglim: float = None,
    rot: float = 0.0,
    timeout: int = 60,
):
    params = {
        "time": utc_time,
        "ra": ra,
        "dec": dec,
        "fov_w": fov_w,
        "fov_h": fov_h,
        "rot": rot,
        "site": site,
        "fmt": "json",
    }
    if maglim is not None:
        params["maglim"] = maglim
    r = requests.get(BASE, params=params, timeout=timeout)
    r.raise_for_status()
    return r.json()
