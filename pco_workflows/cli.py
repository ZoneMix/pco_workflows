import click
from pco_workflows.workflows.parse_authorized_pickups import parse_authorized_pickups
from pco_workflows.workflows.create_csv import create_import_csv
from pco_workflows.workflows.create_episode import create_publishing_episode
from pco_workflows.workflows.delete_all import delete_all_people
from pco_workflows.workflows.delete_fields import delete_field_data
from pco_workflows.workflows.get_field_data import get_field_definition_data
from pco_workflows.workflows.list_fields import list_field_definitions

@click.group()
def cli():
    pass

@cli.command(name="parse-authorized-pickups")
@click.option("--person", required=True, help="Name of the specific person to process authorized pickups for.")
def cli_parse_authorized_pickups(person):
    """Parse authorized pickups for a specific person."""
    clean_authorized_pickups(person)

@cli.command(name="create-csv")
@click.option("--input", required=True, help="Input CSV file path.")
@click.option("--output", required=True, help="Output CSV file path.")
def cli_create_csv(input, output):
    """Transform input CSV for import."""
    create_import_csv(input, output)

@cli.command(name="create-episode")
@click.option("--title", required=True, help="Episode title.")
@click.option("--channel-id", default=None, type=int, help="Channel ID (optional; overrides channel-name if both provided).")
@click.option("--channel-name", default=None, help="Name of the channel to search for and use (optional; if neither ID nor name provided, uses the first channel).")
@click.option("--art", default=None, help="Artwork URL (optional).")
@click.option("--series-id", default=None, type=int, help="Series ID (optional).")
@click.option("--description", default=None, help="Episode description (optional).")
@click.option("--sermon-audio", default=None, help="Sermon audio URL or details (optional).")
@click.option("--stream-type", default=None, help="Stream type (optional, e.g., 'audio' or 'video').")
@click.option("--video-url", default=None, help="Video URL (optional).")
@click.option("--published-to-library-at", default=None, help="Published to library date/time in ISO 8601 format (optional).")
@click.option("--library-audio-url", default=None, help="Library audio URL (optional).")
@click.option("--library-video-url", default=None, help="Library video URL (optional).")
def cli_create_episode(title, channel_id, channel_name, art, series_id, description, sermon_audio, stream_type, video_url, published_to_library_at, library_audio_url, library_video_url):
    """Create a publishing episode with optional attributes and channel search."""
    create_publishing_episode(
        title, channel_id=channel_id, channel_name=channel_name, art=art, series_id=series_id,
        description=description, sermon_audio=sermon_audio, stream_type=stream_type, video_url=video_url,
        published_to_library_at=published_to_library_at, library_audio_url=library_audio_url, library_video_url=library_video_url
    )

@cli.command(name="delete-all")
@click.option("--skip-id", multiple=True, help="Person IDs to skip (can be used multiple times).")
def cli_delete_all(skip_id):
    """Delete all people (with skips)."""
    delete_all_people(list(skip_id))

@cli.command(name="delete-fields")
@click.option("--field", required=True, help="Field name to delete data for.")
def cli_delete_fields(field):
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
