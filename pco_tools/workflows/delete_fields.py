# pco_tools/workflows/delete_fields.py
import click
from pco_tools.api.people import get_field_definition_id, get_field_data
from pco_tools.api.http import api_delete

def delete_field_data(field_name):
    try:
        field_id = get_field_definition_id(field_name)
        params = {"where[field_definition_id]": field_id}
        field_data = get_field_data(params=params)
        total = len(field_data)
        
        if total == 0:
            click.echo(f"No data to delete for field '{field_name}'.")
            return
        
        click.echo(f"Found {total} field data entries to delete for '{field_name}'.")
        
        if not click.confirm(f"Are you sure you want to delete all data for field '{field_name}'? This operation is irreversible and dangerous!"):
            click.echo("Aborted.")
            return
        
        for i, entry in enumerate(field_data, 1):
            api_delete(f"field_data/{entry['id']}")
            click.echo(f"[{i}/{total}] Deleted field data ID {entry['id']}")
    except Exception as e:
        click.echo(f"Error in delete_field_data: {e}", err=True)
