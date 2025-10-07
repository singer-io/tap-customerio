from tap_customerio.streams.abstracts import FullTableStream

class Workspaces(FullTableStream):
    tap_stream_id = "workspaces"
    key_properties = ["id"]
    replication_method = "FULL_TABLE"
    replication_keys = []
    data_key = "workspaces"
    path = "workspaces"
