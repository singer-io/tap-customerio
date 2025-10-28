from tap_customerio.streams.abstracts import FullTableStream

class SubscriptionCenter(FullTableStream):
    tap_stream_id = "subscription_center"
    key_properties = ["id"]
    replication_method = "FULL_TABLE"
    replication_keys = []
    data_key = "topics"
    path = "subscription_topics"

