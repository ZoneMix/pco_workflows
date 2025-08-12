import time
import requests
from requests.exceptions import RequestException
from .auth import get_auth, get_headers

class BaseClient:
    def __init__(self, base):
        self.base = base

    def _full_url(self, url):
        if url.startswith('http'):
            return url
        return f"https://api.planningcenteronline.com/{self.base}/{url.lstrip('/')}"

    def _handle_response(self, resp, method):
        try:
            resp.raise_for_status()
            if method == 'delete' and resp.status_code == 204:
                return None
            return resp.json()
        except RequestException as e:
            error_msg = f"API {method.upper()} failed for {resp.url}: {e}"
            if resp.text:
                error_msg += f" - Response: {resp.text}"
            raise RuntimeError(error_msg)

    def get(self, url, params=None):
        full_url = self._full_url(url)
        resp = requests.get(full_url, auth=get_auth(), headers=get_headers(), params=params)
        return self._handle_response(resp, 'get')

    def post(self, url, data):
        full_url = self._full_url(url)
        resp = requests.post(full_url, auth=get_auth(), headers=get_headers(), json=data)
        return self._handle_response(resp, 'post')

    def patch(self, url, data):
        full_url = self._full_url(url)
        resp = requests.patch(full_url, auth=get_auth(), headers=get_headers(), json=data)
        return self._handle_response(resp, 'patch')

    def delete(self, url):
        full_url = self._full_url(url)
        resp = requests.delete(full_url, auth=get_auth(), headers=get_headers())
        self._handle_response(resp, 'delete')

    def paginate_get(self, url, params=None, extract_key="data"):
        results = []
        current_url = url
        current_params = params or {"per_page": 100}
        while current_url:
            data = self.get(current_url, params=current_params)
            results.extend(data.get(extract_key, []))
            current_url = data.get("links", {}).get("next")
            current_params = None  # Next URL includes params
            time.sleep(0.2)  # Rate limit: ~5 req/sec
        return results
