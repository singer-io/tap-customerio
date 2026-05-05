import json
from typing import Iterator

from tap_customerio.streams.abstracts import FullTableStream


class Activities(FullTableStream):
    tap_stream_id = "activities"
    key_properties = ["id"]
    replication_method = "FULL_TABLE"
    replication_keys = []
    data_key = "activities"
    path = "activities"

    # The /v1/activities endpoint uses a cursor-based pagination scheme where:
    #   - the response carries the next cursor under "next"
    #   - the request must send that cursor as the "start" parameter

    next_page_key = "next"
    next_page_param = "start"

    # The activities endpoint only accepts "limit" (max 100).
    page_size = 100

    def get_records(self) -> Iterator:
        """Paginate the activities endpoint using cursor-based pagination.

        Overrides the base implementation to:
        - use "limit" instead of "page" as the page-size parameter
        - guard against a stuck API (live cursor + empty page → stop)

        Response key: ``next_page_key``  = "next"
        Request key:  ``next_page_param`` = "start"
        """
        self.params["limit"] = self.page_size
        pagination_token = None
        has_more_pages = True

        while has_more_pages:
            if pagination_token:
                self.params[self.next_page_param] = pagination_token
            elif self.next_page_param in self.params:
                # Remove any stale cursor left over from a previous call
                del self.params[self.next_page_param]

            response = self.client.make_request(
                self.http_method,
                self.url_endpoint,
                self.params,
                self.headers,
                body=json.dumps(self.data_payload),
                path=self.path,
            )

            raw_records = response.get(self.data_key) or []
            if not isinstance(raw_records, list):
                raw_records = [raw_records]

            yield from raw_records

            pagination_token = response.get(self.next_page_key)

            # Continue only when the API provides a cursor AND returned records.
            has_more_pages = bool(pagination_token) and bool(raw_records)
