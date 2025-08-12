# pco_tools/workflows/get_field_data.py
import click
from pco_tools.api.people import get_field_definition_id, get_field_data_by_definition, get_people, get_built_in_field_by_name

def get_field_definition_data(field_name):
    try:
        built_in_field = get_built_in_field_by_name(field_name)
        if built_in_field:
            slug = built_in_field['attributes']['slug']
            click.echo(f"Built-in field '{field_name}' (slug: {slug})")
            people = get_people()
            click.echo(f"Data for built-in field '{field_name}':")
            for person in people:
                value = person['attributes'].get(slug, None)
                person_id = person['id']
                person_name = person['attributes'].get("name", None)
                click.echo(f"Person ID: {person_id}, Person Name: {person_name}, Value: {value}")
        else:
            field_id = get_field_definition_id(field_name)
            click.echo(f"Custom field definition ID for '{field_name}': {field_id}")
            field_data = get_field_data_by_definition(field_id)
            click.echo(f"Data for custom field '{field_name}':")
            for entry in field_data:
                value = entry['attributes']['value']
                person_id = entry['relationships']['customizable']['data']['id']
                data_id = entry['id']
                click.echo(f"Person ID: {person_id}, Value: {value}, Field Data ID: {data_id}")
    except ValueError as ve:
        click.echo(f"Field '{field_name}' not found as built-in or custom: {ve}", err=True)
    except Exception as e:
        click.echo(f"Error in get_field_definition_data: {e}", err=True)
