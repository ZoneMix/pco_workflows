# pco_tools/workflows/create_episode.py
import click
from pco_tools.api.http import api_get, api_post

def get_publishing_channel_id():
    params = {"order": "name"}
    channels = api_get("channels", params=params, base="publishing/v2")["data"]
    if not channels:
        raise ValueError("No publishing channels found.")
    return channels[0]["id"]

def create_publishing_episode(title):
    try:
        channel_id = get_publishing_channel_id()
        url = f"channels/{channel_id}/episodes"
        data = {
            "data": {
                "attributes": {
                    "title": title
                }
            }
        }
        response = api_post(url, data, base="publishing/v2")
        click.echo(f"Created episode: {response}")
    except Exception as e:
        click.echo(f"Error in create_publishing_episode: {e}", err=True)
