import click
from pco_workflows.api import PublishingClient

def create_publishing_episode(title):
    client = PublishingClient()
    try:
        channel_id = client.get_first_channel_id()
        url = f"channels/{channel_id}/episodes"
        data = {
            "data": {
                "attributes": {
                    "title": title
                }
            }
        }
        response = client.post(url, data)
        click.echo(f"Created episode: {response}")
    except Exception as e:
        click.echo(f"Error in create_publishing_episode: {e}", err=True)
