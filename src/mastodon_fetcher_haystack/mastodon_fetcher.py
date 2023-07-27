import requests
import html2text
from haystack.nodes import BaseComponent
from haystack.schema import Document
from typing import Optional

class MastodonFetcher(BaseComponent):
    outgoing_edges = 1
    
    def __init__(self, last_k_posts: Optional[int] = 10):
        self.last_k_posts = last_k_posts
        
    def run(self, query: str, last_k_posts: Optional[int] = None):
        if last_k_posts is None:
            last_k_posts = self.last_k_posts
        
        username, instance = query.split('@')
        
        url = f"https://{instance}/api/v1/accounts/lookup?acct={username}"
        try:
            id_response = requests.request("GET", url)
            id = id_response.json()["id"]
            get_status_url = f"https://{instance}/api/v1/accounts/{id}/statuses?limit={last_k_posts}"
            response = requests.request("GET", get_status_url)
            toot_stream = []
            for toot in response.json():
                toot_stream.append(Document(content=html2text.html2text(toot["content"])))
        except Exception as e:
            toot_stream = [Document(content="Please make sure you are providing a correct, publically accesible Mastodon account")]
        
        output = {"documents": toot_stream}
        return output, "output_1"

    def run_batch(self):
        pass