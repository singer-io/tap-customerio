from tap_tester.base_suite_tests.pagination_test import PaginationTest
from base import customerioBaseTest

class customerioPaginationTest(PaginationTest, customerioBaseTest):
    """
    Ensure tap can replicate multiple pages of data for streams that use pagination.
    """

    @staticmethod
    def name():
        return "tap_tester_customerio_pagination_test"

    def streams_to_test(self):
        # Only streams with confirmed multi-page data in the sandbox environment.
        # Full list of excluded streams and reasons are tracked in the test plan.
        return {
            'segments',
            'snippets',
            'info',
        }

