from tap_customerio.streams.abstracts import FullTableStream

class Customers(FullTableStream):
    tap_stream_id = "customers"
    key_properties = ["id"]
    replication_method = "FULL_TABLE"
    replication_keys = []
    data_key = "customers"
    path = "customers/attributes"
    http_method = "POST"
