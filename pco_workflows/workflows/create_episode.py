import click
from pco_workflows.api import PublishingClient

def create_publishing_episode(title, channel_id=None, channel_name=None, art=None, series_id=None, description=None, sermon_audio=None, stream_type=None, video_url=None, published_to_library_at=None, library_audio_url=None, library_video_url=None):
    client = PublishingClient()
    try:
        if channel_name:
            channel_id = client.get_channel_id_by_name(channel_name)
        elif channel_id is None:
            channel_id = client.get_first_channel_id()
        attributes = {
            "channel_id": channel_id,
        }
        if art:
            attributes["art"] = art
        if series_id is not None:
            attributes["series_id"] = int(series_id)
        if description:
            attributes["description"] = description
        if sermon_audio:
            attributes["sermon_audio"] = sermon_audio
        if stream_type:
            attributes["stream_type"] = stream_type
        if video_url:
            attributes["video_url"] = video_url
        if published_to_library_at:
            attributes["published_to_library_at"] = published_to_library_at
        if library_audio_url:
            attributes["library_audio_url"] = library_audio_url
        if library_video_url:
            attributes["library_video_url"] = library_video_url
        response = client.create_episode(title, attributes=attributes)
        click.echo(f"Created episode: {response}")
    except Exception as e:
        click.echo(f"Error in create_publishing_episode: {e}", err=True)
