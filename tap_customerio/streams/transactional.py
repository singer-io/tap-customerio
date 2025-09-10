from tap_customerio.streams.abstracts import IncrementalStream

class Transactional(IncrementalStream):
    tap_stream_id = "transactional"
    key_properties = ["id"]
    replication_method = "INCREMENTAL"
    replication_keys = ["updated_at"]
    data_key = "messages"
    path = "transactional"

