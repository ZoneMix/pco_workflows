# pco_tools/utils.py
import csv
from datetime import datetime

def format_phone(phone):
    if not phone:
        return ""
    digits = ''.join(filter(str.isdigit, phone))
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    return phone

def yes_no_to_true_false(value):
    if not value:
        return ""
    if value.lower() == "yes":
        return "TRUE"
    elif value.lower() == "no":
        return "FALSE"
    return ""

def map_grade(grade):
    if not grade:
        return ""
    grade_lower = grade.lower()
    if "graduated" in grade_lower:
        return ""
    if "pre-school" in grade_lower or "pre-k" in grade_lower:
        return -1
    grade_map = {
        "kindergarten": 0, "first": 1, "second": 2, "third": 3, "fourth": 4,
        "fifth": 5, "sixth": 6, "seventh": 7, "eighth": 8, "ninth": 9,
        "tenth": 10, "eleventh": 11, "twelfth": 12
    }
    for key, value in grade_map.items():
        if key in grade_lower:
            return value
    try:
        num = int(''.join(filter(str.isdigit, grade)))
        if 1 <= num <= 12:
            return num
    except ValueError:
        return ""
    return ""

def get_status_and_membership(member_status):
    if not member_status or member_status.lower() == "no":
        return "Inactive", ""
    return "Active", "Member"

def format_birthdate(birth_month_day, age, current_year=2025):
    if not birth_month_day:
        return ""
    try:
        dt = datetime.strptime(birth_month_day, "%m/%d")
        birth_year = current_year - int(age) if age and age.isdigit() else 1885
        return dt.replace(year=birth_year).strftime("%m/%d/%Y")
    except ValueError:
        return ""

def format_anniversary(wedding_month_day):
    if not wedding_month_day:
        return ""
    try:
        dt = datetime.strptime(wedding_month_day, "%m/%d")
        return dt.replace(year=1885).strftime("%m/%d/%Y")
    except ValueError:
        return ""
