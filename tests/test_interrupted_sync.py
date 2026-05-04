
from base import customerioBaseTest
from tap_tester.base_suite_tests.interrupted_sync_test import InterruptedSyncTest


class customerioInterruptedSyncTest(InterruptedSyncTest, customerioBaseTest):
    """Test tap sets a bookmark and respects it for the next sync of a
    stream."""

    @staticmethod
    def name():
        return "tap_tester_customerio_interrupted_sync_test"

    def streams_to_test(self):
        # Only INCREMENTAL streams that produce records in the sandbox.
        # campaigns excluded: 0 records in sandbox environment.
        return {'segments', 'transactional_messages'}

    def manipulate_state(self):
        # Actual tap sync order is: segments → transactional_messages
        # To satisfy test_interrupted_sync_stream_order:
        #   [0] interrupted    = segments                (currently_syncing, in bookmarks)
        #   [1] already-synced = transactional_messages  (in bookmarks, not currently_syncing)
        return {
            "currently_syncing": "segments",
            "bookmarks": {
                "segments":              {"updated_at": "2020-01-01T00:00:00Z"},
                "transactional_messages": {"updated_at": "2020-01-01T00:00:00Z"},
            }
        }

