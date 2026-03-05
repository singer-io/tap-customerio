import json
from typing import Iterator

from tap_customerio.streams.abstracts import FullTableStream

# Filter that matches every customer (all have a cio_id)
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

        The base-class implementation sends an empty body to
        POST /v1/customers/attributes, which returns an empty list because the
        endpoint requires explicit IDs.
        """
        list_endpoint = f"{self.client.base_url}/customers"
        attrs_endpoint = f"{self.client.base_url}/customers/attributes"
        headers = {**self.headers, "Content-Type": "application/json"}

        list_params = {"limit": self.page_size}
        start_cursor = None

        while True:
            if start_cursor:
                list_params["start"] = start_cursor

            list_response = self.client.make_request(
                "POST",
                list_endpoint,
                list_params,
                headers,
                body=json.dumps(ALL_CUSTOMERS_FILTER),
            )

            ids = list_response.get("ids", [])

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
                yield from attrs_response.get("customers", [])

            start_cursor = list_response.get("next")
            if not start_cursor:
                break
