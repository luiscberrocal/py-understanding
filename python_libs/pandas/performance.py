import timeit
from pathlib import Path

import pandas as pd


def regular_read_csv(csv_file: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_file)
    return df


csv = Path(__file__).parent / 'data' / 'hn.csv'
setup_code = """
from __main__ import regular_read_csv
from pathlib import Path
csv = Path(__file__).home()  / 'PycharmProjects/py-understanding/python_libs/pandas/data/hn.csv'"""
results = timeit.timeit(stmt="regular_read_csv(csv)",
                        setup=setup_code,
                        number=10)
print(results)
