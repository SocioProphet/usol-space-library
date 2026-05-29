import hashlib
import json
import time
from pathlib import Path


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def record_safe_time():
    return time.time()


def write_provenance(path, params: dict, sources: list, stac_item_path: str = None):
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "created_unix": time.time(),
        "created_readable": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
        "params": params,
        "sources": sources,
    }
    output.write_text(json.dumps(record, indent=2))
    if stac_item_path:
        write_stac_item(stac_item_path, params, sources)


def write_stac_item(path, params: dict, sources: list):
    item = {
        "type": "Feature",
        "stac_version": "1.0.0",
        "id": params.get("target", "plate") + "-" + str(int(record_safe_time())),
        "properties": {
            "created": record_safe_time(),
            "usol:params": params,
            "usol:sources": sources,
        },
        "geometry": None,
        "links": [],
        "assets": {},
    }
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(item, indent=2))
