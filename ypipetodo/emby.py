import requests
from urllib.parse import urljoin
from dataclasses import dataclass


@dataclass
class EmbyConnector:
    base_url: str
    token: str
    parent_id: str

    def refresh(self):
        if not self.token:
            return

        url = urljoin(self.base_url, f'/emby/Items/{self.parent_id}/Refresh')
        params = {"Recursive": "true", "api_key": self.token}
        requests.post(url, params =  params).raise_for_status()
