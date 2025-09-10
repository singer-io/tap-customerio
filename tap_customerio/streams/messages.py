from tap_customerio.streams.abstracts import FullTableStream

class Messages(FullTableStream):
    tap_stream_id = "messages"
    key_properties = ["id"]
    replication_method = "FULL_TABLE"
    data_key = "messages"
    path = "messages"
    path = "messages"

