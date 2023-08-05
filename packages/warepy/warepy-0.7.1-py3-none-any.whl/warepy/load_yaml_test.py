import pytest
from . import load_yaml


def test_load_yaml_empty():
    data = load_yaml('warepy/tests/empty.yaml')

    assert \
        data == {}, \
            'Loaded data from an empty yaml should result empty dict'


def test_load_yaml_plain():
    try:
        load_yaml('warepy/tests/plain_type.yaml')
    except TypeError:
        pass
    else:
        raise AssertionError(
            'Loading yaml with plain type should result in TypeError')
