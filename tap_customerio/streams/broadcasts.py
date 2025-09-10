from tap_customerio.streams.abstracts import IncrementalStream

class Broadcasts(IncrementalStream):
    tap_stream_id = "broadcasts"
    key_properties = ["id"]
    replication_method = "INCREMENTAL"
    replication_keys = ["updated_at"]
    data_key = "broadcasts"
    path = "broadcasts"

