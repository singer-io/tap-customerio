from tap_customerio.streams.abstracts import IncrementalStream

class Imports(IncrementalStream):
    tap_stream_id = "imports"
    key_properties = ["id"]
    replication_method = "INCREMENTAL"
    replication_keys = ["updated_at"]
    data_key = None
    path = "imports/1"

    # def parse_response(self, response):
    #     data = response.json()
    #     import_record = data.get("import")
    #     if import_record:
    #         yield import_record