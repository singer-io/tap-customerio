from tap_customerio.streams.abstracts import FullTableStream

class SenderIdentities(FullTableStream):
    tap_stream_id = "sender_identities"
    key_properties = ["id"]
    replication_method = "FULL_TABLE"
    data_key = "sender_identities"
    path = "sender_identities"
    path = "sender_identities"

