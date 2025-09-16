from tap_customerio.streams.abstracts import ChildBaseStream

class Collections(ChildBaseStream):
    tap_stream_id = "collections"
    key_properties = ["id"]
    replication_method = "INCREMENTAL"
    data_key = "collections"
    path = "collections"
    parent = "collections"
    bookmark_value = None

