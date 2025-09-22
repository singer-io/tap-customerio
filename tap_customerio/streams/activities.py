from tap_customerio.streams.abstracts import FullTableStream

class Activities(FullTableStream):
    tap_stream_id = "activities"
    key_properties = ["id"]
    replication_method = "FULL_TABLE"
    replication_keys = []
    data_key = "activities"
    path = "activities"

