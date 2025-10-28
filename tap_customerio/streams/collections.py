from tap_customerio.streams.abstracts import IncrementalStream

class Collections(IncrementalStream):
    tap_stream_id = "collections"
    key_properties = ["id"]
    replication_method = "INCREMENTAL"
    replication_keys = ['updated_at']
    data_key = "collections"
    path = "collections"

