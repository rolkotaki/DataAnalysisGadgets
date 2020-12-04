from datetime import  datetime
from file_management.read_write_files import parse_timestamp


def test_parse_timestamp():
    assert parse_timestamp('2020-06-04 16:33:45') == datetime.strptime('2020-06-04 16:33:45', '%Y-%m-%d %H:%M:%S')


def test_again():
    assert 4 == 4


def test_fail():
    assert 5 == 4

