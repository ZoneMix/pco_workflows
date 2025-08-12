from .client import BaseClient

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

class PeopleClient(BaseClient):
    def __init__(self):
        super().__init__("people/v2")

    def get_people(self, params=None):
        return self.paginate_get("people", params=params)

    def get_person(self, person_id, params=None):
        return self.get(f"people/{person_id}", params=params).get("data")

    def get_addresses_for_person(self, person_id, params=None):
        return self.paginate_get(f"people/{person_id}/addresses", params=params)

    def get_address(self, address_id, params=None):
        return self.get(f"addresses/{address_id}", params=params).get("data")

    def get_emails_for_person(self, person_id, params=None):
        return self.paginate_get(f"people/{person_id}/emails", params=params)

    def get_email(self, email_id, params=None):
        return self.get(f"emails/{email_id}", params=params).get("data")

    def get_phone_numbers_for_person(self, person_id, params=None):
        return self.paginate_get(f"people/{person_id}/phone_numbers", params=params)

    def get_phone_number(self, phone_id, params=None):
        return self.get(f"phone_numbers/{phone_id}", params=params).get("data")

    def get_field_definitions(self, params=None):
        return self.paginate_get("field_definitions", params=params)

    def get_field_definition(self, field_id, params=None):
        return self.get(f"field_definitions/{field_id}", params=params).get("data")

    def get_field_data(self, params=None):
        return self.paginate_get("field_data", params=params)

    def get_field_datum(self, field_data_id, params=None):
        return self.get(f"field_data/{field_data_id}", params=params).get("data")

    def get_field_data_for_person(self, person_id, params=None):
        return self.paginate_get(f"people/{person_id}/field_data", params=params)

    def get_households(self, params=None):
        return self.paginate_get("households", params=params)

    def get_household(self, household_id, params=None):
        return self.get(f"households/{household_id}", params=params).get("data")

    def get_birthdays(self, params=None):
        return self.paginate_get("birthdays", params=params)

    def get_anniversaries(self, params=None):
        return self.paginate_get("anniversaries", params=params)

    # Utilities
    def get_all_people_ids(self):
        people = self.get_people()
        return [p["id"] for p in people]

    def get_field_definition_id(self, field_name):
        defs = self.get_field_definitions({"where[name]": field_name})
        if not defs:
            raise ValueError(f"Field definition '{field_name}' not found.")
        return defs[0]["id"]

    def get_field_data_by_definition(self, field_definition_id):
        return self.get_field_data({"where[field_definition_id]": field_definition_id})

    def search_person_by_name(self, search_name):
        people = self.get_people({"where[search_name]": search_name, "per_page": 1})
        if not people:
            return "", ""
        person_id = people[0]["id"]
        emails = self.get_emails_for_person(person_id)
        email = emails[0]["attributes"]["address"] if emails else ""
        phones = self.get_phone_numbers_for_person(person_id)
        phone = phones[0]["attributes"]["number"] if phones else ""
        return email, phone

