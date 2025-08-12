# pco_tools/workflows/list_fields.py
import click
from pco_tools.api.people import get_field_definitions, BUILT_IN_FIELDS

def list_field_definitions():
    try:
        custom_fields = get_field_definitions()
        
        click.echo("Built-in Field Definitions:")
        click.echo("{:<30} {:<20} {:<15}".format("Name", "Slug", "Data Type"))
        click.echo("-" * 85)
        # Sort built-in fields alphabetically by name for better UX
        for f in sorted(BUILT_IN_FIELDS, key=lambda x: x['attributes']['name']):
            attrs = f['attributes']
            click.echo("{:<30} {:<20} {:<15}".format(
                attrs['name'][:28] + '...' if len(attrs['name']) > 28 else attrs['name'],
                attrs['slug'][:18] + '...' if len(attrs['slug']) > 18 else attrs['slug'],
                attrs['data_type'],
            ))
        
        click.echo("\nCustom Field Definitions:")
        click.echo("{:<10} {:<30} {:<20} {:<15} {:<10}".format("ID", "Name", "Slug", "Data Type", "Sequence"))
        click.echo("-" * 85)
        if not custom_fields:
            click.echo("No custom field definitions found.")
        else:
            for f in sorted(custom_fields, key=lambda x: x['attributes']['sequence'] or 0):
                attrs = f['attributes']
                click.echo("{:<10} {:<30} {:<20} {:<15} {:<10}".format(
                    f['id'],
                    attrs['name'][:28] + '...' if len(attrs['name']) > 28 else attrs['name'],
                    attrs['slug'][:18] + '...' if len(attrs['slug']) > 18 else attrs['slug'],
                    attrs['data_type'],
                    attrs['sequence'] or 'N/A'  # Fallback here too, though usually an int
                ))
    except Exception as e:
        click.echo(f"Error listing field definitions: {e}", err=True)
