from tap_customerio.streams.abstracts import FullTableStream

class Objects(FullTableStream):
    tap_stream_id = "objects"
    key_properties = ["id"]
    replication_method = "FULL_TABLE"
    data_key = "types"
    path = "object_types"
    path = "objects"

