from tap_customerio.streams.abstracts import FullTableStream

class Workspaces(FullTableStream):
    tap_stream_id = "workspaces"
    key_properties = ["id"]
    replication_method = "FULL_TABLE"
    data_key = "Workspaces"
    path = "Workspaces"
    path = "Workspaces"

