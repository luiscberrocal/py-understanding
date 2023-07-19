import timeit
from pathlib import Path

import pandas as pd


def regular_read_csv(csv_file: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_file)
    return df


def py_arrow_read_csv(csv_file: Path) -> pd.DataFrame:
    df_arrow = pd.read_csv(csv_file, engine='pyarrow', dtype_backend='pyarrow')
    return df_arrow


csv = Path(__file__).parent / 'data' / 'hn.csv'
setup_code = """
from __main__ import regular_read_csv, py_arrow_read_csv 
from pathlib import Path
csv = Path(__file__).home()  / 'PycharmProjects/py-understanding/python_libs/pandas/data/hn.csv'"""

results1 = timeit.timeit(stmt="regular_read_csv(csv)",
                        setup=setup_code,
                        number=10)
print(f'regular_read_csv: {results1:.2f} seconds')

results2 = timeit.timeit(stmt="py_arrow_read_csv(csv)",
                         setup=setup_code,
                         number=10)
print(f'py_arrow_read_csv: {results2:.2f} seconds')
