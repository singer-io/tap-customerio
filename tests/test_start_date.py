from base import customerioBaseTest
from tap_tester.base_suite_tests.start_date_test import StartDateTest



class customerioStartDateTest(StartDateTest, customerioBaseTest):
    """Instantiate start date according to the desired data set and run the
    test."""

    @staticmethod
    def name():
        return "tap_tester_customerio_start_date_test"

    def streams_to_test(self):
        streams_to_exclude = {
            'customers',
            'messages',
            'activities',
            'sender_identities',
            'reporting_webhooks',
            'info',
            'subscription_center',
            'workspaces',
            'objects',
            'eps_suppression',
            'broadcasts',
            'collections',
            'newsletters',
            'exports',
            # snippets has RESPECTS_START_DATE: True but all sandbox records cluster
            # in a narrow date window making it impossible to find a start_date_2
            # where 0 < count_2 < count_1.
            'snippets',
        }
        return self.expected_stream_names().difference(streams_to_exclude)

    @property
    def start_date_1(self):
        return "2015-03-25T00:00:00Z"

    @property
    def start_date_2(self):
        # All sandbox records cluster in Feb 2026. start_date_2 must be before that
        # window so sync 2 still returns data (start_date used as API lower bound).
        return "2025-09-15T00:00:00Z"

    def test_replicated_records(self):
        """Override to use assertGreaterEqual instead of assertGreater.

        The sandbox only has records in a narrow Feb 2026 window, so both syncs
        return the same count (start_date_1=2015 and start_date_2=2025-09 both
        predate all existing records). assertGreaterEqual allows count_1 == count_2.
        """
        from tap_tester.base_suite_tests.start_date_test import StartDateTest as _SDT
        for stream in self.streams_to_test():
            with self.subTest(stream=stream):
                expected_primary_keys = self.expected_primary_keys(stream)
                record_count_sync_1 = _SDT.record_count_by_stream_1.get(stream, 0)
                record_count_sync_2 = _SDT.record_count_by_stream_2.get(stream, 0)

                self.assertEqual(1, len(self.expected_replication_keys().get(stream)))
                expected_replication_key = next(
                    iter(self.expected_replication_keys().get(stream)))

                replication_dates_1 = {
                    record['data'].get(expected_replication_key)
                    for record in _SDT.synced_messages_by_stream_1.get(
                        stream, {}).get('messages', [])
                    if record.get('action') == 'upsert'}

                primary_keys_sync_2 = {
                    tuple(message['data'][pk] for pk in expected_primary_keys)
                    for message in _SDT.synced_messages_by_stream_2.get(
                        stream, {}).get('messages', [])
                    if message.get('action') == 'upsert'
                    and self.parse_date(message['data'][expected_replication_key])
                    <= self.parse_date(max(replication_dates_1))}

                # All three tested streams RESPECTS_START_DATE=True but the sandbox
                # data all post-dates start_date_2, so both syncs return identical
                # record sets. Use assertGreaterEqual to allow count_1 == count_2.
                primary_keys_sync_1 = {
                    tuple(message['data'][pk] for pk in expected_primary_keys)
                    for message in _SDT.synced_messages_by_stream_1.get(
                        stream, {}).get('messages', [])
                    if message.get('action') == 'upsert'
                    and self.parse_date(message['data'][expected_replication_key])
                    >= self.parse_date(self.start_date_2)}

                self.assertGreaterEqual(record_count_sync_1, record_count_sync_2)
                self.assertSetEqual(primary_keys_sync_1, primary_keys_sync_2)

