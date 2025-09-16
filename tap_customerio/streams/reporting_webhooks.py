from tap_customerio.streams.abstracts import ChildBaseStream

class ReportingWebhooks(ChildBaseStream):
    tap_stream_id = "reporting_webhooks"
    key_properties = ["id"]
    replication_method = "INCREMENTAL"
    data_key = "reporting_webhooks"
    path = "reporting_webhooks"
    parent = "reporting_webhooks"
    bookmark_value = None

