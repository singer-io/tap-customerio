from tap_customerio.streams.abstracts import FullTableStream

class Info(FullTableStream):
    tap_stream_id = "info"
    key_properties = ["id"]
    replication_method = "FULL_TABLE"
    data_key = "ip_addresses"
    path = "info/ip_addresses"
    path = "ip_addresses"

