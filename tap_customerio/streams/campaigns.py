from tap_customerio.streams.abstracts import ChildBaseStream

class Campaigns(ChildBaseStream):
    tap_stream_id = "campaigns"
    key_properties = ["id"]
    replication_method = "INCREMENTAL"
    replication_keys = ["updated_at"]
    data_key = "campaigns"
    path = "campaigns"
    parent = "campaigns"
    bookmark_value = None

