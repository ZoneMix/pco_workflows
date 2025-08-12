import time
import requests
from requests.exceptions import RequestException
from .auth import get_auth, get_headers

class BaseClient:
    def __init__(self, base):
        self.base = base

    def _full_url(self, url):
        if url.startswith('http'):
            return url
        return f"https://api.planningcenteronline.com/{self.base}/{url.lstrip('/')}"

    def _handle_response(self, resp, method):
        try:
            resp.raise_for_status()
            if method == 'delete' and resp.status_code == 204:
                return None
            return resp.json()
        except RequestException as e:
            error_msg = f"API {method.upper()} failed for {resp.url}: {e}"
            if resp.text:
                error_msg += f" - Response: {resp.text}"
            raise RuntimeError(error_msg)

    def get(self, url, params=None):
        full_url = self._full_url(url)
        resp = requests.get(full_url, auth=get_auth(), headers=get_headers(), params=params)
        return self._handle_response(resp, 'get')

    def post(self, url, data):
        full_url = self._full_url(url)
        resp = requests.post(full_url, auth=get_auth(), headers=get_headers(), json=data)
        return self._handle_response(resp, 'post')

    def patch(self, url, data):
        full_url = self._full_url(url)
        resp = requests.patch(full_url, auth=get_auth(), headers=get_headers(), json=data)
        return self._handle_response(resp, 'patch')

    def delete(self, url):
        full_url = self._full_url(url)
        resp = requests.delete(full_url, auth=get_auth(), headers=get_headers())
        self._handle_response(resp, 'delete')

    def paginate_get(self, url, params=None, extract_key="data"):
        results = []
        current_url = url
        current_params = params or {"per_page": 100}
        while current_url:
            data = self.get(current_url, params=current_params)
            results.extend(data.get(extract_key, []))
            current_url = data.get("links", {}).get("next")
            current_params = None  # Next URL includes params
            time.sleep(0.2)  # Rate limit: ~5 req/sec
        return results

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
