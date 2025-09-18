from typing import Dict, Iterator, List
from singer import get_logger
from tap_customerio.streams.abstracts import FullTableStream

class EpsSuppression(FullTableStream):
    tap_stream_id = "eps_suppression"
    key_properties = ["id"]
    replication_method = "FULL_TABLE"
    replication_keys = []
    data_key = "suppressions"
    path = "esp/search_suppression/{email_address}"
    parent = "esp"

    def get_url_endpoint(self, parent_obj: Dict = None) -> str:
        """EpsSuppression the API endpoint URL for fetching."""
        if not parent_obj or 'id' not in parent_obj:
            raise ValueError("parent_obj must be provided with an 'email' key.")
        return f"{self.client.base_url}/{self.path.format(email_address = parent_obj['id'])}"