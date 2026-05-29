from usolspace.horizons_parser import parse_table


def test_parse_empty():
    import pandas as pd

    df = parse_table("")
    assert isinstance(df, pd.DataFrame)
    assert df.empty
