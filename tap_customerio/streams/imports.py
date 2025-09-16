from tap_customerio.streams.abstracts import ChildBaseStream

class Imports(ChildBaseStream):
    tap_stream_id = "imports"
    key_properties = ["id"]
    replication_method = "INCREMENTAL"
    data_key = "import"
    path = "imports"
    parent = "imports"
    bookmark_value = None

