from tap_customerio.streams.abstracts import ChildBaseStream

class Newsletters(ChildBaseStream):
    tap_stream_id = "newsletters"
    key_properties = ["id"]
    replication_method = "INCREMENTAL"
    replication_keys = ["updated_at"]
    data_key = "newsletters"
    path = "newsletters"
    parent = "newsletters"
    bookmark_value = None

