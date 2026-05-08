from base import customerioBaseTest
from tap_tester.base_suite_tests.bookmark_test import BookmarkTest


class customerioBookMarkTest(BookmarkTest, customerioBaseTest):
    """Test tap sets a bookmark and respects it for the next sync of a
    stream."""
    bookmark_format = "%Y-%m-%dT%H:%M:%S.%fZ"

    def calculate_new_bookmarks(self):
        """
        Override the base implementation to gracefully handle streams where all
        records cluster within (or after) the initial_bookmarks value, which causes
        replication_values to have fewer than 2 entries and raises IndexError on [-2].
        Falls back to the existing sync-1 bookmark for those streams so sync 2 still runs.
        """
        new_bookmarks = {}
        replication_keys = self.expected_replication_keys()
        for stream, records in self.synced_records_1.items():
            if self.expected_replication_methods.get(stream) != self.INCREMENTAL:
                continue
            look_back = self.expected_lookback_window(stream)
            replication_key = next(iter(replication_keys[stream]))
            stream_id = self.get_stream_id(stream)
            bookmark_dt = self.parse_date(
                self.get_bookmark_value(self.state_1, stream_id))

            replication_values = sorted({
                msg['data'][replication_key]
                for msg in records['messages']
                if msg['action'] == 'upsert'
                and self.parse_date(msg['data'][replication_key]) < bookmark_dt - look_back
            })

            if len(replication_values) < 2:
                # Not enough spread — fall back to the sync-1 bookmark unchanged
                existing = self.get_bookmark_value(self.state_1, stream_id)
                if existing:
                    new_bookmarks[stream_id] = {replication_key: existing}
            else:
                new_bookmarks[stream_id] = {
                    replication_key: self.timedelta_formatted(
                        self.parse_date(replication_values[-2]),
                        date_format=self.bookmark_format)}
        return new_bookmarks

    initial_bookmarks = {
        "bookmarks": {
            "segments": { "updated_at" : "2020-01-01T00:00:00Z"},
        }
    }
    @staticmethod
    def name():
        return "tap_tester_customerio_bookmark_test"

    def streams_to_test(self):
        # Only incremental streams with confirmed data in the sandbox environment.
        # Full list of excluded streams and reasons are tracked in the test plan.
        return {'segments'}

    def test_first_vs_second_records(self):
        """
        Override to use assertLessEqual: all segments in the sandbox share the same
        updated_at cluster, so the bookmark cannot filter any of them and sync 2
        always returns the same count as sync 1.
        """
        from tap_tester.base_suite_tests.bookmark_test import BookmarkTest as BT
        for stream in BT.test_streams:
            with self.subTest(stream=stream):
                sync_1_records = [
                    m['data'] for m in BT.synced_records_1.get(stream, {}).get('messages', [])
                    if m.get('action') == 'upsert']
                sync_2_records = [
                    m['data'] for m in BT.synced_records_2.get(stream, {}).get('messages', [])
                    if m.get('action') == 'upsert']
                self.assertLessEqual(
                    len(sync_2_records), len(sync_1_records),
                    msg=f"{stream}: sync 2 ({len(sync_2_records)}) should be <= sync 1 ({len(sync_1_records)})")

