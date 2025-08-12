# pco_tools/workflows/parse_authorized_pickups.py
import click
from pco_tools.api.people import get_field_definition_id, search_person_by_name, get_field_data_for_person, get_people
from pco_tools.api.http import api_post, api_patch

def parse_authorized_pickups(person_name):
    try:
        auth_pickup_id = get_field_definition_id("Authorized Pickups")
        auth_pickup_parsed_id = get_field_definition_id("Authorized Pickups Parsed")
        
        # Search for the person
        people = get_people({"where[search_name]": person_name, "per_page": 1})
        if not people:
            click.echo(f"No person found with name '{person_name}'")
            return
        person_id = people[0]["id"]
        
        # Get field data for the person
        field_data = get_field_data_for_person(person_id, {"where[field_definition_id]": auth_pickup_id})
        if not field_data:
            click.echo(f"No 'Authorized Pickups' data found for person '{person_name}' (ID: {person_id})")
            return
        
        for entry in field_data:
            values = [v.strip() for v in entry["attributes"]["value"].split(",") if v.strip()]
            processed_values = []
            for name in values:
                email, phone = search_person_by_name(name)
                if not email:
                    email = 0
                if not phone:
                    phone = 0
                processed_values.append(f"{name};{email};{phone}")
            entry_value = '|'.join(processed_values)
            if entry_value and not entry_value.endswith('|'):
                entry_value += '|'
            
            # Check for existing parsed field data
            existing_parsed = get_field_data_for_person(person_id, {"where[field_definition_id]": auth_pickup_parsed_id})
            payload = {
                "data": {
                    "attributes": {
                        "field_definition_id": auth_pickup_parsed_id,
                        "value": entry_value
                    }
                }
            }
            if existing_parsed:
                # Update existing (assume single entry)
                field_data_id = existing_parsed[0]["id"]
                url = f"field_data/{field_data_id}"
                api_patch(url, payload)
                click.echo(f"Updated existing parsed entry for person {person_id}: {entry_value}")
            else:
                # Create new
                url = f"people/{person_id}/field_data"
                api_post(url, payload)
                click.echo(f"Created parsed entry for person {person_id}: {entry_value}")
    except Exception as e:
        click.echo(f"Error in clean_authorized_pickups: {e}", err=True)
