
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
        # Return streams in deterministic order to match the actual tap sync order:
        # campaigns → segments → transactional_messages
        return ['campaigns', 'segments', 'transactional_messages']

    def manipulate_state(self):
        # Actual tap sync order is: campaigns → segments → transactional_messages
        # To satisfy test_interrupted_sync_stream_order:
        #   [0] interrupted  = campaigns         (currently_syncing, in bookmarks)
        #   [1] not-yet-synced = segments        (absent from bookmarks)
        #   [2] already-synced = transactional_messages (in bookmarks, not currently_syncing)
        return {
            "currently_syncing": "campaigns",
            "bookmarks": {
                "campaigns":             {"updated":    "2020-01-01T00:00:00Z"},
                "transactional_messages": {"updated_at": "2020-01-01T00:00:00Z"},
            }
        }

