from tap_customerio.streams.abstracts import ChildBaseStream

class Snippets(ChildBaseStream):
    tap_stream_id = "snippets"
    key_properties = ["snippet_name"]
    replication_method = "INCREMENTAL"
    data_key = "snippets"
    path = "snippets"
    parent = "snippets"
    bookmark_value = None

