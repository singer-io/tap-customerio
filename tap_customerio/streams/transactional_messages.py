from tap_customerio.streams.abstracts import IncrementalStream

class TransactionalMessages(IncrementalStream):
    tap_stream_id = "transactional_messages"
    key_properties = ["id"]
    replication_method = "INCREMENTAL"
    replication_keys = ["updated_at"]
    data_key = "messages"
    path = "transactional"


