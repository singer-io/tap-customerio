from tap_customerio.streams.abstracts import FullTableStream

class ReportingWebhooks(FullTableStream):
    tap_stream_id = "reporting_webhooks"
    key_properties = ["id"]
    replication_method = "FULL_TABLE"
    data_key = "reporting_webhooks"
    path = "reporting_webhooks"

