from base import customerioBaseTest
from tap_tester.base_suite_tests.all_fields_test import AllFieldsTest

KNOWN_MISSING_FIELDS = {

}


class customerioAllFields(AllFieldsTest, customerioBaseTest):
    """Ensure running the tap with all streams and fields selected results in
    the replication of all fields."""

    @staticmethod
    def name():
        return "tap_tester_customerio_all_fields_test"

    def streams_to_test(self):
        # streams_to_exclude = {
        #     "sender_identities",
        #     "customers",
        #     "eps_suppression",
        #     "collections",
        #     "broadcasts",
        #     "messages",
        #     "subscription_center",
        #
        # }
        # return self.expected_stream_names().difference(streams_to_exclude)
        return {"newsletters"}

