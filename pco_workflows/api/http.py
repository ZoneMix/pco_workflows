# pco_tools/api/http.py
import time
import requests
from requests.exceptions import RequestException
from .auth import get_auth, get_headers

def api_get(url, params=None, base="people/v2"):
    """
    Perform a GET request to the PCO API.
    Handles absolute URLs for pagination links.
    """
    if url.startswith('http'):
        full_url = url
    else:
        base_url = f"https://api.planningcenteronline.com/{base}"
        full_url = f"{base_url}/{url.lstrip('/')}"
    auth = get_auth()
    headers = get_headers()
    try:
        resp = requests.get(full_url, auth=auth, headers=headers, params=params)
        resp.raise_for_status()
        return resp.json()
    except RequestException as e:
        error_msg = f"API GET failed for {full_url}: {e}"
        if 'resp' in locals():
            error_msg += f" - Response: {resp.text}"
        raise RuntimeError(error_msg)

def api_post(url, data, base="people/v2"):
    """
    Perform a POST request to the PCO API.
    """
    if url.startswith('http'):
        full_url = url
    else:
        base_url = f"https://api.planningcenteronline.com/{base}"
        full_url = f"{base_url}/{url.lstrip('/')}"
    auth = get_auth()
    headers = get_headers()
    try:
        resp = requests.post(full_url, auth=auth, headers=headers, json=data)
        resp.raise_for_status()
        return resp.json()
    except RequestException as e:
        error_msg = f"API POST failed for {full_url}: {e}"
        if 'resp' in locals():
            error_msg += f" - Response: {resp.text}"
        raise RuntimeError(error_msg)

def api_patch(url, data, base="people/v2"):
    """
    Perform a PATCH request to the PCO API.
    """
    if url.startswith('http'):
        full_url = url
    else:
        base_url = f"https://api.planningcenteronline.com/{base}"
        full_url = f"{base_url}/{url.lstrip('/')}"
    auth = get_auth()
    headers = get_headers()
    try:
        resp = requests.patch(full_url, auth=auth, headers=headers, json=data)
        resp.raise_for_status()
        return resp.json()
    except RequestException as e:
        error_msg = f"API PATCH failed for {full_url}: {e}"
        if 'resp' in locals():
            error_msg += f" - Response: {resp.text}"
        raise RuntimeError(error_msg)

def api_delete(url, base="people/v2"):
    """
    Perform a DELETE request to the PCO API.
    """
    if url.startswith('http'):
        full_url = url
    else:
        base_url = f"https://api.planningcenteronline.com/{base}"
        full_url = f"{base_url}/{url.lstrip('/')}"
    auth = get_auth()
    headers = get_headers()
    try:
        resp = requests.delete(full_url, auth=auth, headers=headers)
        if resp.status_code != 204:
            raise ValueError(f"Delete failed with status {resp.status_code}: {resp.text}")
    except RequestException as e:
        error_msg = f"API DELETE failed for {full_url}: {e}"
        if 'resp' in locals():
            error_msg += f" - Response: {resp.text}"
        raise RuntimeError(error_msg)

def paginate_get(url, params=None, base="people/v2", extract_key="data"):
    """
    Paginate through a list endpoint, collecting all results.
    Supports PCO's offset/per_page pagination.
    """
    results = []
    current_url = url
    current_params = params or {"per_page": 100}
    while current_url:
        data = api_get(current_url, params=current_params, base=base)
        results.extend(data.get(extract_key, []))
        current_url = data.get("links", {}).get("next")
        current_params = None  # Next URL includes params
        time.sleep(0.2)  # Rate limit: ~5 req/sec
    return results
