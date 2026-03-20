import json
from typing import Iterator

from tap_customerio.streams.abstracts import FullTableStream

# Filter that matches every *tracked* customer in the workspace.
#
# Assumption: ``cio_id`` is assigned to every profile that has been
# explicitly identified via the Customer.io identify call or an import.
# Anonymous/untracked profiles (those that have only been observed through
# page-view events and have never been identified) will NOT have a ``cio_id``
# set in all workspace configurations and will therefore be excluded from this
# filter.
#
# If your workspace tracks anonymous profiles that should also be exported,
# replace or extend this filter to suit your requirements, or make the filter
# configurable via tap config.
ALL_CUSTOMERS_FILTER = {
    "filter": {
        "and": [{"attribute": {"field": "cio_id", "operator": "exists"}}]
    }
}
# Number of IDs to resolve per POST /customers/attributes call
ATTRIBUTES_BATCH_SIZE = 100


class Customers(FullTableStream):
    tap_stream_id = "customers"
    key_properties = ["id"]
    replication_method = "FULL_TABLE"
    replication_keys = []
    data_key = "customers"
    path = "customers/attributes"
    http_method = "POST"

    def get_records(self) -> Iterator:
        """
        The Customer.io API requires a two-step approach to retrieve all customers:

        Step 1 – POST /v1/customers
            Supply a broad filter and paginate via the `start` cursor parameter to
            collect all customer IDs.

        Step 2 – POST /v1/customers/attributes
            Pass the IDs collected in step 1 (in batches) to retrieve full customer
            attribute records.

        The base-class implementation sends a request body that lacks the required
        `ids` field (for example, an empty JSON object) to POST /v1/customers/attributes,
        which returns an empty list because the endpoint requires explicit IDs.
        """
        list_endpoint = f"{self.client.base_url}/customers"
        attrs_endpoint = f"{self.client.base_url}/customers/attributes"
        headers = {**self.headers, "Content-Type": "application/json"}

        list_params = {"limit": self.page_size}
        start_cursor = None
        has_more_pages = True
        page_number = 0

        while has_more_pages:
            if start_cursor:
                list_params["start"] = start_cursor

            page_number += 1
            list_response = self.client.make_request(
                "POST",
                list_endpoint,
                list_params,
                headers,
                body=json.dumps(ALL_CUSTOMERS_FILTER),
            )

            ids = list_response.get("ids") or []

            # Fetch full attributes in batches
            for i in range(0, len(ids), ATTRIBUTES_BATCH_SIZE):
                batch_ids = ids[i : i + ATTRIBUTES_BATCH_SIZE]
                attrs_response = self.client.make_request(
                    "POST",
                    attrs_endpoint,
                    {},
                    headers,
                    body=json.dumps({"ids": batch_ids}),
                )
                customers = attrs_response.get("customers") or []
                if not isinstance(customers, list):
                    customers = [customers]
                yield from customers

            start_cursor = list_response.get("next")

            # Continue only when the API provides a cursor AND returned IDs.
            has_more_pages = bool(start_cursor) and bool(ids)
