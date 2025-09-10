from tap_customerio.streams.abstracts import ChildBaseStream

class Segments(ChildBaseStream):
    tap_stream_id = "segments"
    key_properties = ["id"]
    replication_method = "INCREMENTAL"
    replication_keys = ["updated_at"]
    data_key = "segments"
    path = "segments"
    parent = "segments"
    bookmark_value = None

