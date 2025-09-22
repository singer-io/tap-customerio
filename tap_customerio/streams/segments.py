from tap_customerio.streams.abstracts import IncrementalStream

class Segments(IncrementalStream):
    tap_stream_id = "segments"
    key_properties = ["id"]
    replication_method = "INCREMENTAL"
    replication_keys = ["updated_at"]
    data_key = "segments"
    path = "segments"

