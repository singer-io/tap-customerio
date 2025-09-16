from tap_customerio.streams.abstracts import ChildBaseStream

class Customers(ChildBaseStream):
    tap_stream_id = "customers"
    key_properties = ["id"]
    replication_method = "INCREMENTAL"
    replication_keys = ["updated_at"]
    data_key = "customers"
    path = "customers/attributes"
    parent = "customers"
    bookmark_value = None

