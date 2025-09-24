import json
from typing import Iterator

from tap_customerio.streams.abstracts import IncrementalStream

class Newsletters(IncrementalStream):
    tap_stream_id = "newsletters"
    key_properties = ["id"]
    replication_method = "INCREMENTAL"
    replication_keys = ["updated"]
    data_key = "newsletters"
    path = "newsletters"

    def get_records(self) -> Iterator:
        next_page = None
        while True:
            params = {}
            if next_page:
                params["start"] = next_page  # correct param for cursor
            response = self.client.make_request(
                self.http_method,
                self.url_endpoint,
                params=params,
                headers=self.headers,
                body=json.dumps(self.data_payload) if self.data_payload else None,
                path=self.path
            )

            raw_records = response.get(self.data_key, []) or []
            yield from raw_records

            next_page = response.get("next")
            if not next_page:
                break

