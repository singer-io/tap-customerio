from tap_customerio.streams.abstracts import IncrementalStream

class Exports(IncrementalStream):
    tap_stream_id = "exports"
    key_properties = ["id"]
    replication_method = "INCREMENTAL"
    replication_keys = ["updated_at"]
    data_key = "exports"
    path = "exports"