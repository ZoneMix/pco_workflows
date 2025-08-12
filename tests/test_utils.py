# tests/test_utils.py
import pytest
from pco_tools.utils import format_phone, yes_no_to_true_false, map_grade, get_status_and_membership, format_birthdate, format_anniversary

def test_format_phone():
    assert format_phone("1234567890") == "(123) 456-7890"
    assert format_phone("abc") == "abc"
    assert format_phone("") == ""

def test_yes_no_to_true_false():
    assert yes_no_to_true_false("yes") == "TRUE"
    assert yes_no_to_true_false("no") == "FALSE"
    assert yes_no_to_true_false("maybe") == ""
    assert yes_no_to_true_false("") == ""

def test_map_grade():
    assert map_grade("First Grade") == 1
    assert map_grade("Pre-K") == -1
    assert map_grade("Graduated") == ""
    assert map_grade("12th") == 12
    assert map_grade("College") == ""

def test_get_status_and_membership():
    assert get_status_and_membership("yes") == ("Active", "Member")
    assert get_status_and_membership("no") == ("Inactive", "")
    assert get_status_and_membership("") == ("Inactive", "")

def test_format_birthdate():
    assert format_birthdate("01/01", "10", 2025) == "01/01/2015"
    assert format_birthdate("invalid", "10") == ""
    assert format_birthdate("", "10") == ""

def test_format_anniversary():
    assert format_anniversary("01/01") == "01/01/1885"
    assert format_anniversary("invalid") == ""
    assert format_anniversary("") == ""
