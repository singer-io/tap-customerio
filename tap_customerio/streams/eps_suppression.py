from tap_customerio.streams.abstracts import FullTableStream

class EpsSuppression(FullTableStream):
    tap_stream_id = "eps_suppression"
    key_properties = ["id"]
    replication_method = "FULL_TABLE"
    replication_keys = []
    data_key = "suppressions"
    path = "esp/search_suppression/1"

