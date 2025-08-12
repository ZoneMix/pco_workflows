import click
from pco_workflows.workflows.parse_authorized_pickups import parse_authorized_pickups
from pco_workflows.workflows.create_csv import create_import_csv
from pco_workflows.workflows.create_episode import create_publishing_episode
from pco_workflows.workflows.delete_all import delete_all_people
from pco_workflows.workflows.delete_field import delete_field_data
from pco_workflows.workflows.get_field_data import get_field_definition_data
from pco_workflows.workflows.list_fields import list_field_definitions

@click.group()
def cli():
    pass

@cli.command(name="parse-authorized-pickups")
@click.option("--person", required=True, help="Name of the specific person to process authorized pickups for.")
def cli_parse_authorized_pickups(person):
    """Parse authorized pickups for a specific person."""
    parse_authorized_pickups(person)

@cli.command(name="create-csv")
@click.option("--input", required=True, help="Input CSV file path.")
@click.option("--output", required=True, help="Output CSV file path.")
def cli_create_csv(input, output):
    """Transform input CSV for import."""
    create_import_csv(input, output)

@cli.command(name="create-episode")
@click.option("--title", default="New Episode", help="Episode title.")
def cli_create_episode(title):
    """Create a publishing episode."""
    create_publishing_episode(title)

@cli.command(name="delete-all")
@click.option("--skip-id", multiple=True, help="Person IDs to skip (can be used multiple times).")
def cli_delete_all(skip_id):
    """Delete all people (with skips)."""
    delete_all_people(list(skip_id))

@cli.command(name="delete-birthdays")
def cli_delete_birthdays():
    """Set all birthdays to null."""
    delete_birthdays()

@cli.command(name="delete-field")
@click.option("--field", required=True, help="Field name to delete data for.")
def cli_delete_field(field):
    """Delete all data for a specific field."""
    delete_field_data(field)

@cli.command(name="get-field-data")
@click.option("--field", required=True, help="Field name to get data for.")
def cli_get_field_data(field):
    """Get data for a specific field."""
    get_field_definition_data(field)

@cli.command(name="list-fields")
def cli_list_fields():
    """List all available field definitions."""
    list_field_definitions()

if __name__ == "__main__":
    cli()
