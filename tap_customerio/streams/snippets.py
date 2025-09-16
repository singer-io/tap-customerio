from tap_customerio.streams.abstracts import IncrementalStream

class Snippets(IncrementalStream):
    tap_stream_id = "snippets"
    key_properties = ["snippet_name"]
    replication_method = "INCREMENTAL"
    replication_keys = ['updated_at']
    data_key = "snippets"
    path = "snippets"

