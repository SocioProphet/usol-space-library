# JPL Horizons API (JSON)

Authoritative doc: https://ssd-api.jpl.nasa.gov/doc/horizons.html

Typical parameters:
- `format=json`
- `COMMAND`: NAIF/SPK or name, e.g. `499` for Mars
- `OBJ_DATA=YES|NO`
- `MAKE_EPHEM=YES|NO`
- `EPHEM_TYPE=OBSERVER|VECTORS`
- `CENTER`, e.g. `500@399` geocenter or site code
- `START_TIME`, `STOP_TIME`, `STEP_SIZE`
- `QUANTITIES`, e.g. `1,9,20`

Endpoint:
`https://ssd-api.jpl.nasa.gov/api/horizons.api`

Notes:
- JSON payload wraps text blocks; see `result` and `error` fields.
- Use `usolspace.horizons_parser.parse_table(result_text)` to convert a Horizons `result` block into a DataFrame.
