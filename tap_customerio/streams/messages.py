from tap_customerio.streams.abstracts import FullTableStream

class Messages(FullTableStream):
    tap_stream_id = "messages"
    key_properties = ["id"]
    replication_method = "FULL_TABLE"
    replication_keys = []
    data_key = "messages"
    path = "messages"

