from tap_customerio.streams.abstracts import IncrementalStream

class Imports(IncrementalStream):
    tap_stream_id = "imports"
    key_properties = ["id"]
    replication_method = "INCREMENTAL"
    replication_keys = ["updated_at"]
    data_key = None
    path = "imports/1"