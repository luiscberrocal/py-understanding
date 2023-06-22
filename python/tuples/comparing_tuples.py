from python.tuples.adapters import version_str_to_tuple


def compare_tuples_gt():
    versions = ['5.2.6', '5.2.7', '5.3.0a1', '5.3.0b1', '5.3.0b2', '5.3.0rc1', '5.3.0']
    versions_tuples = [version_str_to_tuple(x) for x in versions]
    print(versions_tuples)
    for i, vt in enumerate(versions_tuples[:-1], 1):
        comparison_str = f'{versions_tuples[i]} > {vt}'
        try:
            result = versions_tuples[i] > vt
            print(f'{comparison_str:30} = {result}')
        except TypeError:
            print(f'{comparison_str:30} = ERROR')


def compare_tuple_lt(bigger_version: str, smaller_version: str) -> None:
    bigger_tuple = version_str_to_tuple(bigger_version)
    smaller_tuple = version_str_to_tuple(smaller_version)
    result = smaller_tuple < bigger_tuple
    comparison_str = f'{smaller_tuple} < {bigger_tuple}'
    print(f'{comparison_str:30} = {result}')


if __name__ == '__main__':
    # compare_tuples_gt()
    compare_tuple_lt('5.3.0', '5.3.0rc1')
