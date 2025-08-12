# pco_tools/api/people.py
from .http import api_get, paginate_get

BUILT_IN_FIELDS = [
    {
        "id": None,
        "attributes": {
            "name": "First Name",
            "slug": "first_name",
            "data_type": "string",
            "sequence": None
        }
    },
    {
        "id": None,
        "attributes": {
            "name": "Middle Name",
            "slug": "middle_name",
            "data_type": "string",
            "sequence": None
        }
    },
    {
        "id": None,
        "attributes": {
            "name": "Last Name",
            "slug": "last_name",
            "data_type": "string",
            "sequence": None
        }
    },
    {
        "id": None,
        "attributes": {
            "name": "Nickname",
            "slug": "nickname",
            "data_type": "string",
            "sequence": None
        }
    },
    {
        "id": None,
        "attributes": {
            "name": "Birthdate",
            "slug": "birthdate",
            "data_type": "date",
            "sequence": None
        }
    },
    {
        "id": None,
        "attributes": {
            "name": "Anniversary",
            "slug": "anniversary",
            "data_type": "date",
            "sequence": None
        }
    },
    {
        "id": None,
        "attributes": {
            "name": "Gender",
            "slug": "gender",
            "data_type": "string",
            "sequence": None
        }
    },
    {
        "id": None,
        "attributes": {
            "name": "Grade",
            "slug": "grade",
            "data_type": "integer",
            "sequence": None
        }
    },
    {
        "id": None,
        "attributes": {
            "name": "Child",
            "slug": "child",
            "data_type": "boolean",
            "sequence": None
        }
    },
    {
        "id": None,
        "attributes": {
            "name": "Graduation Year",
            "slug": "graduation_year",
            "data_type": "integer",
            "sequence": None
        }
    },
    {
        "id": None,
        "attributes": {
            "name": "Medical Notes",
            "slug": "medical_notes",
            "data_type": "text",
            "sequence": None
        }
    },
    {
        "id": None,
        "attributes": {
            "name": "Membership",
            "slug": "membership",
            "data_type": "string",
            "sequence": None
        }
    },
    {
        "id": None,
        "attributes": {
            "name": "Status",
            "slug": "status",
            "data_type": "string",
            "sequence": None
        }
    },
    {
        "id": None,
        "attributes": {
            "name": "School Type",
            "slug": "school_type",
            "data_type": "string",
            "sequence": None
        }
    },
    {
        "id": None,
        "attributes": {
            "name": "Passed Background Check",
            "slug": "passed_background_check",
            "data_type": "boolean",
            "sequence": None
        }
    },
    # Add more if needed, but these are the main editable ones
]

def get_built_in_field_slugs():
    return [f['attributes']['slug'] for f in BUILT_IN_FIELDS]

def get_built_in_field_by_name(field_name):
    for f in BUILT_IN_FIELDS:
        if f['attributes']['name'].lower() == field_name.lower():
            return f
    return None

# People Resource Endpoints

def get_people(params=None):
    """
    GET /people/v2/people
    List all people. Supports pagination.
    Query params: offset, per_page, where[search_name], where[status], include (e.g., emails,addresses), order (e.g., last_name).
    Example: get_people({"where[search_name]": "John"})
    Returns list of person dicts.
    """
    return paginate_get("people", params=params)

def get_person(person_id, params=None):
    """
    GET /people/v2/people/{person_id}
    Get a single person by ID.
    Query params: include (e.g., emails,phone_numbers,field_data).
    No pagination.
    Example: get_person(12345, {"include": "emails"})
    Returns person dict.
    """
    return api_get(f"people/{person_id}", params=params).get("data")

# Addresses Resource Endpoints

def get_addresses_for_person(person_id, params=None):
    """
    GET /people/v2/people/{person_id}/addresses
    List addresses for a person. Supports pagination.
    Query params: offset, per_page, order.
    Example: get_addresses_for_person(12345)
    Returns list of address dicts.
    """
    return paginate_get(f"people/{person_id}/addresses", params=params)

def get_address(address_id, params=None):
    """
    GET /people/v2/addresses/{address_id}
    Get a single address by ID.
    No pagination.
    Example: get_address(67890)
    Returns address dict.
    """
    return api_get(f"addresses/{address_id}", params=params).get("data")

# Emails Resource Endpoints

def get_emails_for_person(person_id, params=None):
    """
    GET /people/v2/people/{person_id}/emails
    List emails for a person. Supports pagination.
    Query params: offset, per_page, order.
    Example: get_emails_for_person(12345)
    Returns list of email dicts.
    """
    return paginate_get(f"people/{person_id}/emails", params=params)

def get_email(email_id, params=None):
    """
    GET /people/v2/emails/{email_id}
    Get a single email by ID.
    No pagination.
    Example: get_email(11121)
    Returns email dict.
    """
    return api_get(f"emails/{email_id}", params=params).get("data")

# Phone Numbers Resource Endpoints

def get_phone_numbers_for_person(person_id, params=None):
    """
    GET /people/v2/people/{person_id}/phone_numbers
    List phone numbers for a person. Supports pagination.
    Query params: offset, per_page, order.
    Example: get_phone_numbers_for_person(12345)
    Returns list of phone number dicts.
    """
    return paginate_get(f"people/{person_id}/phone_numbers", params=params)

def get_phone_number(phone_id, params=None):
    """
    GET /people/v2/phone_numbers/{phone_id}
    Get a single phone number by ID.
    No pagination.
    Example: get_phone_number(13141)
    Returns phone number dict.
    """
    return api_get(f"phone_numbers/{phone_id}", params=params).get("data")

# Field Definitions Resource Endpoints

def get_field_definitions(params=None):
    """
    GET /people/v2/field_definitions
    List all custom field definitions. Supports pagination.
    Query params: offset, per_page, where[name], order.
    Example: get_field_definitions({"where[name]": "Authorized Pickups"})
    Returns list of field definition dicts.
    """
    return paginate_get("field_definitions", params=params)

def get_field_definition(field_id, params=None):
    """
    GET /people/v2/field_definitions/{field_id}
    Get a single field definition by ID.
    No pagination.
    Example: get_field_definition(932227)
    Returns field definition dict.
    """
    return api_get(f"field_definitions/{field_id}", params=params).get("data")

# Field Data Resource Endpoints

def get_field_data(params=None):
    """
    GET /people/v2/field_data
    List all custom field data entries (across people). Supports pagination.
    Query params: offset, per_page, where[field_definition_id], order.
    Example: get_field_data({"where[field_definition_id]": 932227})
    Returns list of field data dicts.
    """
    return paginate_get("field_data", params=params)

def get_field_datum(field_data_id, params=None):
    """
    GET /people/v2/field_data/{field_data_id}
    Get a single field data entry by ID.
    No pagination.
    Example: get_field_datum(15161)
    Returns field data dict.
    """
    return api_get(f"field_data/{field_data_id}", params=params).get("data")

def get_field_data_for_person(person_id, params=None):
    """
    GET /people/v2/people/{person_id}/field_data
    List custom field data for a specific person. Supports pagination.
    Query params: offset, per_page, where[field_definition_id], order.
    Example: get_field_data_for_person(12345)
    Returns list of field data dicts for the person.
    """
    return paginate_get(f"people/{person_id}/field_data", params=params)

# Households Resource Endpoints

def get_households(params=None):
    """
    GET /people/v2/households
    List all households. Supports pagination.
    Query params: offset, per_page, where[name], include (e.g., people), order.
    Example: get_households({"where[name]": "Smith Household"})
    Returns list of household dicts.
    """
    return paginate_get("households", params=params)

def get_household(household_id, params=None):
    """
    GET /people/v2/households/{household_id}
    Get a single household by ID.
    Query params: include (e.g., people).
    No pagination.
    Example: get_household(17181, {"include": "people"})
    Returns household dict.
    """
    return api_get(f"households/{household_id}", params=params).get("data")

# Specialized List Endpoints

def get_birthdays(params=None):
    """
    GET /people/v2/birthdays
    List upcoming birthdays (e.g., for a month). Supports pagination.
    Query params: offset, per_page (defaults to 31 for a month), where[month].
    Example: get_birthdays({"per_page": 31})
    Returns list of person dicts with birthdays.
    """
    return paginate_get("birthdays", params=params)

def get_anniversaries(params=None):
    """
    GET /people/v2/anniversaries
    List upcoming anniversaries. Supports pagination.
    Query params: offset, per_page (defaults to 31), where[month].
    Example: get_anniversaries({"per_page": 31})
    Returns list of person dicts with anniversaries.
    """
    return paginate_get("anniversaries", params=params)

# Utility Functions (from your original code, refactored to use above)

def get_all_people_ids():
    """
    Fetch all people IDs using pagination.
    """
    people = get_people()
    return [p["id"] for p in people]

def get_field_definition_id(field_name):
    """
    Get field definition ID by name.
    Uses where[name] filter.
    Raises ValueError if not found.
    """
    defs = get_field_definitions({"where[name]": field_name})
    if not defs:
        raise ValueError(f"Field definition '{field_name}' not found.")
    return defs[0]["id"]

def get_field_data_by_definition(field_definition_id):
    """
    Fetch field data for a specific field definition.
    """
    return get_field_data({"where[field_definition_id]": field_definition_id})

def search_person_by_name(search_name):
    """
    Search for a person by name and return first match's email and phone.
    Returns ("", "") if not found.
    """
    people = get_people({"where[search_name]": search_name, "per_page": 1})
    if not people:
        return "", ""
    person_id = people[0]["id"]
    
    emails = get_emails_for_person(person_id)
    email = emails[0]["attributes"]["address"] if emails else ""
    
    phones = get_phone_numbers_for_person(person_id)
    phone = phones[0]["attributes"]["number"] if phones else ""
    
    return email, phone
