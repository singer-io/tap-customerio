from base import customerioBaseTest
from tap_tester.base_suite_tests.all_fields_test import AllFieldsTest


class customerioAllFields(AllFieldsTest, customerioBaseTest):
    """Ensure running the tap with all streams and fields selected results in
    the replication of all fields."""

    # Fields present in the schema but not returned by the sandbox environment
    MISSING_FIELDS = {
        "campaigns": {"event_type", "event_name", "filter_segment_ids"},
    }

    @staticmethod
    def name():
        return "tap_tester_customerio_all_fields_test"

    def streams_to_test(self):
        streams_to_exclude = {
            'eps_suppression',
            'subscription_center',
            'sender_identities',
            'broadcasts',
            'customers',
            'collections',
            'messages',
            'newsletters',
            # No records exist in the sandbox environment for these streams
            'exports',
            'objects',
            'reporting_webhooks',
        }
        return self.expected_stream_names().difference(streams_to_exclude)

