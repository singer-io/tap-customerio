from tap_customerio.streams.abstracts import ChildBaseStream

class Exports(ChildBaseStream):
    tap_stream_id = "exports"
    key_properties = ["id"]
    replication_method = "INCREMENTAL"
    replication_keys = ["updated_at"]
    data_key = "exports"
    path = "exports"
    parent = "exports"
    bookmark_value = None

