from typing import Dict, Iterator, List
import json
from tap_customerio.streams.abstracts import FullTableStream


class EpsSuppression(FullTableStream):
    tap_stream_id = "eps_suppression"
    key_properties = ["email"]
    replication_method = "FULL_TABLE"
    replication_keys = []
    data_key = "suppressions"
    path = "esp/suppression/{suppression_type}"

    def get_records(self) -> Iterator[Dict]:
        suppression_types = ["bounces", "spam_reports"]
        self.params["page"] = self.page_size
        for suppression_type in suppression_types:
            path = self.path.format(suppression_type=suppression_type)
            next_page = 1

            while next_page:
                response = self.client.make_request(
                    method="GET",
                    endpoint=None,
                    path=path,
                    params=self.params,
                    headers=self.headers,
                    body=None
                )
                raw_records = response.get(self.data_key) or []
                for record in raw_records:
                    record["suppression_type"] = suppression_type
                yield from raw_records
                next_page = response.get(self.next_page_key)
                self.params[self.next_page_key] = next_page
