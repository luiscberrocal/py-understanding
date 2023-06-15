from typing import List

from python.tuples.adapters import version_str_to_tuple


def compare_tuples():
    versions = ['5.2.6', '5.2.7', '5.3.0a1', '5.3.0b1', '5.3.0b2', '5.3.0rc1', '5.3.0']
    versions_tuples = [version_str_to_tuple(x) for x in versions]
    print(versions_tuples)
    fo


if __name__ == '__main__':
    compare_tuples()