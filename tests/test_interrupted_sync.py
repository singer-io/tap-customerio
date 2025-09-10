
from base import customerioBaseTest
from tap_tester.base_suite_tests.interrupted_sync_test import InterruptedSyncTest


class customerioInterruptedSyncTest(customerioBaseTest):
    """Test tap sets a bookmark and respects it for the next sync of a
    stream."""

    @staticmethod
    def name():
        return "tap_tester_customerio_interrupted_sync_test"

    def streams_to_test(self):
        return self.expected_stream_names()


    def manipulate_state(self):
        return {
            "currently_syncing": "prospects",
            "bookmarks": {
                "broadcasts": { "updated_at" : "2020-01-01T00:00:00Z"},
                "transactional": { "updated_at" : "2020-01-01T00:00:00Z"},
                "customers": { "updated_at" : "2020-01-01T00:00:00Z"},
                "campaigns": { "updated_at" : "2020-01-01T00:00:00Z"},
                "newsletters": { "updated_at" : "2020-01-01T00:00:00Z"},
                "segments": { "updated_at" : "2020-01-01T00:00:00Z"},
                "exports": { "updated_at" : "2020-01-01T00:00:00Z"},
        }
    }

