import re
import pandas as pd

_TABLE_START = re.compile(r'^\$\$SOE')
_TABLE_END = re.compile(r'^\$\$EOE')


def parse_table(result_text: str) -> pd.DataFrame:
    """Parse Horizons JSON 'result' text into a DataFrame.

    The parser looks for the $$SOE ... $$EOE block and splits CSV-like lines.
    Column names depend on QUANTITIES; when a matching header appears before
    $$SOE, the parser applies it.
    """
    if not result_text:
        return pd.DataFrame()

    lines = result_text.splitlines()
    try:
        i0 = next(i for i, line in enumerate(lines) if _TABLE_START.search(line))
        i1 = next(i for i, line in enumerate(lines) if i > i0 and _TABLE_END.search(line))
    except StopIteration:
        return pd.DataFrame()

    header = None
    for j in range(max(0, i0 - 10), i0):
        if "Date__(UT)__HR:MN:SC" in lines[j] or "Date__(UT)__HR:MN" in lines[j]:
            header = [h.strip() for h in re.split(r",\s*", lines[j].strip())]
            break

    data_lines = []
    for line in lines[i0 + 1:i1]:
        line = line.strip()
        if not line or line.startswith('!'):
            continue
        parts = [part.strip() for part in line.strip(',').split(',')]
        data_lines.append(parts)

    if not data_lines:
        return pd.DataFrame()

    max_len = max(len(row) for row in data_lines)
    rows = [row + [''] * (max_len - len(row)) for row in data_lines]
    df = pd.DataFrame(rows)
    if header and len(header) == df.shape[1]:
        df.columns = header
    return df
