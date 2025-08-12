import click
from pco_workflows.api import PeopleClient
from pco_workflows.api.people import BUILT_IN_FIELDS

def list_field_definitions():
    client = PeopleClient()
    try:
        custom_fields = client.get_field_definitions()
        
        click.echo("Built-in Field Definitions:")
        click.echo("{:<10} {:<30} {:<20} {:<15} {:<10}".format("ID", "Name", "Slug", "Data Type", "Sequence"))
        click.echo("-" * 85)
        for f in sorted(BUILT_IN_FIELDS, key=lambda x: x['attributes']['name']):
            attrs = f['attributes']
            click.echo("{:<10} {:<30} {:<20} {:<15} {:<10}".format(
                f.get('id', 'N/A'),
                attrs['name'][:28] + '...' if len(attrs['name']) > 28 else attrs['name'],
                attrs['slug'][:18] + '...' if len(attrs['slug']) > 18 else attrs['slug'],
                attrs['data_type'],
                attrs['sequence'] or 'N/A'
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
                    attrs['sequence'] or 'N/A'
                ))
    except Exception as e:
        click.echo(f"Error listing field definitions: {e}", err=True)
