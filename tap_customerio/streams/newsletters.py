from tap_customerio.streams.abstracts import IncrementalStream

class Newsletters(IncrementalStream):
    tap_stream_id = "newsletters"
    key_properties = ["id"]
    replication_method = "INCREMENTAL"
    replication_keys = ["updated"]
    data_key = "newsletters"
    path = "newsletters"
    next_page_param = "start"

