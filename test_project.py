from project import parse_frequency, to_per_year, parse_relation
import pytest
def test_frequency():
    assert parse_frequency("twice a week")==(2,'week')
    assert parse_frequency("every day")==(1,'day')
    assert parse_frequency("once a year")==(1,'year')
def test_year():
    assert to_per_year(1,'day')==365
    assert to_per_year(1,'week')==52
    assert to_per_year(1,'month')==12
def test_relation():
    assert parse_relation('grandmother')=='grandparent'
    assert parse_relation('friend')=='friend'
    assert parse_relation('child')=='child'
    assert parse_relation('wife')=='partner'
    assert parse_relation('mother')=='parent'
    assert parse_relation('sister')=='sibling'