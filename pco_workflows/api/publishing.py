from .client import BaseClient

class PublishingClient(BaseClient):
    def __init__(self):
        super().__init__("publishing/v2")

    def get_channels(self, params=None):
        return self.paginate_get("channels", params=params)

    def get_channel(self, channel_id, params=None):
        return self.get(f"channels/{channel_id}", params=params).get("data")

    def get_channel_id_by_name(self, name):
        channels = self.get_channels({"where[name]": name, "per_page": 1})
        if not channels:
            raise ValueError(f"No channel found with name '{name}'")
        return channels[0]["id"]

    def get_first_channel_id(self):
        channels = self.get_channels({"order": "name", "per_page": 1})
        if not channels:
            raise ValueError("No channels found.")
        return channels[0]["id"]

    def create_episode(self, title, channel_id, attributes=None):
        payload = {
            "data": {
                "attributes": {
                    "title": title,
                    "channel_id": channel_id,
                    **(attributes or {})
                }
            }
        }
        return self.post("episodes", payload).get("data")

    def get_episodes(self, channel_id, params=None):
        return self.paginate_get(f"channels/{channel_id}/episodes", params=params)

    def get_episode(self, episode_id, params=None):
        return self.get(f"episodes/{episode_id}", params=params).get("data")

    def update_episode(self, episode_id, attributes):
        payload = {
            "data": {
                "attributes": attributes
            }
        }
        return self.patch(f"episodes/{episode_id}", payload).get("data")

    def delete_episode(self, episode_id):
        self.delete(f"episodes/{episode_id}")

    def get_episode_resources(self, episode_id, params=None):
        return self.paginate_get(f"episodes/{episode_id}/episode_resources", params=params)

    def get_episode_resource(self, resource_id, params=None):
        return self.get(f"episode_resources/{resource_id}", params=params).get("data")

    def create_episode_resource(self, episode_id, attributes):
        payload = {
            "data": {
                "attributes": attributes
            }
        }
        return self.post(f"episodes/{episode_id}/episode_resources", payload).get("data")

    def update_episode_resource(self, resource_id, attributes):
        payload = {
            "data": {
                "attributes": attributes
            }
        }
        return self.patch(f"episode_resources/{resource_id}", payload).get("data")

    def delete_episode_resource(self, resource_id):
        self.delete(f"episode_resources/{resource_id}")
