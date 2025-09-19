from tap_customerio.streams.abstracts import IncrementalStream

class Customers(IncrementalStream):
    tap_stream_id = "customers"
    key_properties = ["id"]
    replication_method = "INCREMENTAL"
    replication_keys = ["updated_at"]
    data_key = "customers"
    path = "customers/attributes"
    http_method = "POST"
