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

    # The /v1/activities response returns the next-page cursor under the key
    # "next", but the REQUEST must pass that value as "start" — not "next".
    # The base-class get_records() uses next_page_key for both reading the
    # cursor from the response AND as the request parameter name, so we must
    # override get_records() here to apply the correct parameter mapping.
    #
    # Additionally, the base class sets params["page"] = page_size (1000), but
    # the activities endpoint only recognises "limit" (max 100).

    _LIMIT = 100  # maximum page size accepted by the activities endpoint

    def get_records(self) -> Iterator:
        """Paginate the activities endpoint using cursor-based pagination.

        Response key: "next"  (cursor for the next page)
        Request key:  "start" (cursor to begin the next page from)
        """
        self.params["limit"] = self._LIMIT
        next_cursor = None  # No cursor on the first request

        while True:
            if next_cursor:
                self.params["start"] = next_cursor
            elif "start" in self.params:
                # Clean up any stale cursor from a previous call
                del self.params["start"]

            response = self.client.make_request(
                self.http_method,
                self.url_endpoint,
                self.params,
                self.headers,
                body=json.dumps(self.data_payload),
                path=self.path,
            )

            raw_records = response.get(self.data_key) or []
            next_cursor = response.get("next")  # may be None on the last page
            yield from raw_records

            if not next_cursor:
                break

