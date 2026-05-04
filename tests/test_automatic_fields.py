"""Test that with no fields selected for a stream automatic fields are still
replicated."""
from base import customerioBaseTest
from tap_tester.base_suite_tests.automatic_fields_test import MinimumSelectionTest


class customerioAutomaticFields(MinimumSelectionTest, customerioBaseTest):
    """Test that with no fields selected for a stream automatic fields are
    still replicated."""

    @staticmethod
    def name():
        return "tap_tester_customerio_automatic_fields_test"

    def streams_to_test(self):
        # Only streams confirmed to have data in the sandbox environment.
        # Full list of excluded streams and reasons are tracked in the test plan.
        return {
            'transactional_messages',
            'segments',
            'workspaces',
            'snippets',
            'info',
        }

