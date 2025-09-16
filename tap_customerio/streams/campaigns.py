from tap_customerio.streams.abstracts import IncrementalStream

class Campaigns(IncrementalStream):
    tap_stream_id = "campaigns"
    key_properties = ["id"]
    replication_method = "INCREMENTAL"
    replication_keys = ["updated"]
    # replication_keys = ["updated_at"]
    data_key = "campaigns"
    path = "campaigns"


