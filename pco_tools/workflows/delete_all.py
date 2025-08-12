# pco_tools/workflows/delete_all.py
import click
import time
from pco_tools.api.people import get_all_people_ids
from pco_tools.api.http import api_delete

def delete_all_people(skip_ids):
    try:
        people_ids = get_all_people_ids()
        skip_set = set(skip_ids)
        to_delete = [pid for pid in people_ids if pid not in skip_set]
        total = len(to_delete)
        
        if total == 0:
            click.echo("No people to delete.")
            return
        
        click.echo(f"Found {total} people to delete (skipping {len(skip_set)}).")
        
        if not click.confirm("Are you sure you want to delete these people? This operation is irreversible and dangerous!"):
            click.echo("Aborted.")
            return
        
        for i, pid in enumerate(to_delete, 1):
            api_delete(f"people/{pid}")
            click.echo(f"[{i}/{total}] Deleted person ID {pid}")
            time.sleep(0.2)
    except Exception as e:
        click.echo(f"Error in delete_all_people: {e}", err=True)
