from base import customerioBaseTest
from tap_tester.base_suite_tests.bookmark_test import BookmarkTest


class customerioBookMarkTest(BookmarkTest, customerioBaseTest):
    """Test tap sets a bookmark and respects it for the next sync of a
    stream."""
    bookmark_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    initial_bookmarks = {
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
    @staticmethod
    def name():
        return "tap_tester_customerio_bookmark_test"

    def streams_to_test(self):
        streams_to_exclude = {}
        return self.expected_stream_names().difference(streams_to_exclude)

