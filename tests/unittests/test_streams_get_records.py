"""Unit tests for Activities.get_records(), Customers.get_records(), and Newsletters.get_records().

Covers:
 - Cursor-based pagination (single and multi-page)
 - Correct request parameters (limit, start) across pages
 - Termination conditions (no cursor, empty cursor, empty records)
 - Infinite-loop guard (empty page returned with a live cursor)
 - Null-safe handling when API returns null for ids / customers keys
 - Two-step flow in Customers (list IDs → fetch attributes in batches)
 - Content-Type header propagation after authenticate() merge fix
 - Newsletters: updated_since bookmark filter forwarded via self.params
"""
import json
import unittest
from unittest.mock import MagicMock, patch
from parameterized import parameterized

from tap_customerio.streams.activities import Activities
from tap_customerio.streams.customers import (
    ALL_CUSTOMERS_FILTER,
    Customers,
)
from tap_customerio.streams.newsletters import Newsletters


class ConcreteActivities(Activities):
    """Concrete Activities with required abstract properties satisfied."""

    @property
    def tap_stream_id(self):
        return "activities"

    @property
    def replication_method(self):
        return "FULL_TABLE"

    @property
    def replication_keys(self):
        return []

    @property
    def key_properties(self):
        return ["id"]


class ConcreteCustomers(Customers):
    """Concrete Customers with required abstract properties satisfied."""

    @property
    def tap_stream_id(self):
        return "customers"

    @property
    def replication_method(self):
        return "FULL_TABLE"

    @property
    def replication_keys(self):
        return []

    @property
    def key_properties(self):
        return ["id"]



# ---------------------------------------------------------------------------
# Activities tests
# ---------------------------------------------------------------------------

class TestActivitiesGetRecords(unittest.TestCase):
    """Tests for Activities.get_records() cursor-based pagination."""

    @patch("tap_customerio.streams.abstracts.metadata.to_map")
    def setUp(self, mock_to_map):
        mock_catalog = MagicMock()
        mock_catalog.schema.to_dict.return_value = {}
        mock_catalog.metadata = []
        mock_to_map.return_value = {}

        mock_client = MagicMock()
        mock_client.base_url = "https://api.customer.io/v1"

        self.stream = ConcreteActivities(client=mock_client, catalog=mock_catalog)

    def test_single_page_returns_all_records(self):
        """A response with no 'next' cursor yields records and stops."""
        self.stream.client.make_request.return_value = {
            "activities": [{"id": 1}, {"id": 2}],
        }

        records = list(self.stream.get_records())

        self.assertEqual(records, [{"id": 1}, {"id": 2}])
        self.assertEqual(self.stream.client.make_request.call_count, 1)

    def test_multi_page_yields_all_records_in_order(self):
        """Pagination across two pages yields records from both pages."""
        self.stream.client.make_request.side_effect = [
            {"activities": [{"id": 1}, {"id": 2}], "next": "cursor-page2"},
            {"activities": [{"id": 3}]},
        ]

        records = list(self.stream.get_records())

        self.assertEqual([r["id"] for r in records], [1, 2, 3])
        self.assertEqual(self.stream.client.make_request.call_count, 2)

    def test_second_page_request_contains_start_cursor(self):
        """The 'next' value from page 1 must be sent as 'start' on page 2."""
        self.stream.client.make_request.side_effect = [
            {"activities": [{"id": 1}], "next": "cursor-abc"},
            {"activities": []},
        ]

        list(self.stream.get_records())

        _, _, second_call_params, *_ = self.stream.client.make_request.call_args_list[1][0]
        self.assertEqual(second_call_params.get("start"), "cursor-abc")

    def test_first_request_does_not_include_start_param(self):
        """The very first request must not carry a 'start' parameter."""
        self.stream.client.make_request.return_value = {"activities": []}

        list(self.stream.get_records())

        _, _, first_call_params, *_ = self.stream.client.make_request.call_args[0]
        self.assertNotIn("start", first_call_params)

    def test_limit_param_is_always_100(self):
        """Every request must use limit=100 (max accepted by activities endpoint)."""
        self.stream.client.make_request.return_value = {"activities": []}

        list(self.stream.get_records())

        _, _, params, *_ = self.stream.client.make_request.call_args[0]
        self.assertEqual(params.get("limit"), 100)

    @parameterized.expand([
        ["none_cursor",  None],
        ["empty_cursor", ""],
    ])
    def test_falsy_next_cursor_terminates_pagination(self, name, cursor_value):
        """Both None and '' as 'next' values must stop iteration after one page."""
        self.stream.client.make_request.return_value = {
            "activities": [{"id": 1}],
            "next": cursor_value,
        }

        records = list(self.stream.get_records())

        self.assertEqual(len(records), 1)
        self.assertEqual(self.stream.client.make_request.call_count, 1)

    def test_infinite_loop_guard_empty_page_with_live_cursor(self):
        """If the API returns no records but a live cursor, we must stop — not loop."""
        self.stream.client.make_request.return_value = {
            "activities": [],
            "next": "stuck-cursor",
        }

        records = list(self.stream.get_records())

        self.assertEqual(records, [])
        self.assertEqual(self.stream.client.make_request.call_count, 1)

    @parameterized.expand([
        ["key_absent",   {}],
        ["key_is_null",  {"activities": None}],
        ["key_is_empty", {"activities": []}],
    ])
    def test_missing_or_null_data_key_returns_empty_list(self, name, response):
        """None or absent data_key must not raise TypeError and yields nothing."""
        self.stream.client.make_request.return_value = response

        records = list(self.stream.get_records())

        self.assertEqual(records, [])


# ---------------------------------------------------------------------------
# Customers tests
# ---------------------------------------------------------------------------

class TestCustomersGetRecords(unittest.TestCase):
    """Tests for Customers.get_records() two-step ETL (list IDs → attributes)."""

    @patch("tap_customerio.streams.abstracts.metadata.to_map")
    def setUp(self, mock_to_map):
        mock_catalog = MagicMock()
        mock_catalog.schema.to_dict.return_value = {}
        mock_catalog.metadata = []
        mock_to_map.return_value = {}

        mock_client = MagicMock()
        mock_client.base_url = "https://api.customer.io/v1"

        self.stream = ConcreteCustomers(client=mock_client, catalog=mock_catalog)
        self.list_url  = "https://api.customer.io/v1/customers"
        self.attrs_url = "https://api.customer.io/v1/customers/attributes"

    def test_single_page_single_batch_returns_records(self):
        """Step 1 returns two IDs; step 2 returns two customer records."""
        self.stream.client.make_request.side_effect = [
            {"ids": ["id-1", "id-2"], "next": None},
            {"customers": [{"id": "id-1"}, {"id": "id-2"}]},
        ]

        records = list(self.stream.get_records())

        self.assertEqual([r["id"] for r in records], ["id-1", "id-2"])
        self.assertEqual(self.stream.client.make_request.call_count, 2)

    def test_list_endpoint_called_before_attributes_endpoint(self):
        """Step 1 (list) must always precede step 2 (attributes)"""
        self.stream.client.make_request.side_effect = [
            {"ids": ["id-1"], "next": None},
            {"customers": [{"id": "id-1"}]},
        ]

        list(self.stream.get_records())

        first_call_url  = self.stream.client.make_request.call_args_list[0][0][1]
        second_call_url = self.stream.client.make_request.call_args_list[1][0][1]
        self.assertEqual(first_call_url,  self.list_url)
        self.assertEqual(second_call_url, self.attrs_url)

    def test_multi_page_list_cursor_forwarded_to_next_request(self):
        """The 'next' cursor from list page 1 must appear as 'start' in list page 2."""
        self.stream.client.make_request.side_effect = [
            {"ids": ["a"], "next": "cursor-page2"},
            {"customers": [{"id": "a"}]},
            {"ids": ["b"], "next": None},
            {"customers": [{"id": "b"}]},
        ]

        records = list(self.stream.get_records())

        self.assertEqual([r["id"] for r in records], ["a", "b"])
        list_page2_params = self.stream.client.make_request.call_args_list[2][0][2]
        self.assertEqual(list_page2_params.get("start"), "cursor-page2")

    def test_ids_exceeding_batch_size_split_into_multiple_attribute_requests(self):
        """150 IDs must produce 2 attribute requests (batch size = 100)."""
        ids = [str(i) for i in range(150)]
        self.stream.client.make_request.side_effect = [
            {"ids": ids, "next": None},
            {"customers": [{"id": str(i)} for i in range(100)]},
            {"customers": [{"id": str(i)} for i in range(100, 150)]},
        ]

        records = list(self.stream.get_records())

        self.assertEqual(len(records), 150)
        # 1 list call + 2 batched attribute calls
        self.assertEqual(self.stream.client.make_request.call_count, 3)

    def test_infinite_loop_guard_empty_ids_with_live_cursor(self):
        """If list endpoint returns empty ids with a live cursor, we must stop."""
        self.stream.client.make_request.return_value = {
            "ids": [],
            "next": "stuck-cursor",
        }

        records = list(self.stream.get_records())

        self.assertEqual(records, [])
        self.assertEqual(self.stream.client.make_request.call_count, 1)

    @parameterized.expand([
        ["ids_absent",   {"next": None}],
        ["ids_is_null",  {"ids": None, "next": None}],
        ["ids_is_empty", {"ids": [],   "next": None}],
    ])
    def test_null_or_missing_ids_no_attribute_request_made(self, name, list_response):
        """Null / absent / empty ids must yield nothing and skip the attributes call."""
        self.stream.client.make_request.return_value = list_response

        records = list(self.stream.get_records())

        self.assertEqual(records, [])
        self.assertEqual(self.stream.client.make_request.call_count, 1)

    @parameterized.expand([
        ["customers_absent",   {}],
        ["customers_is_null",  {"customers": None}],
        ["customers_is_empty", {"customers": []}],
    ])
    def test_null_or_missing_customers_in_attrs_response_no_crash(self, name, attrs_response):
        """Null / absent 'customers' in attributes response must not raise TypeError."""
        self.stream.client.make_request.side_effect = [
            {"ids": ["x"], "next": None},
            attrs_response,
        ]

        records = list(self.stream.get_records())

        self.assertEqual(records, [])

    def test_list_request_body_uses_all_customers_filter(self):
        """POST /customers body must contain the ALL_CUSTOMERS_FILTER payload."""
        self.stream.client.make_request.return_value = {"ids": [], "next": None}

        list(self.stream.get_records())

        list_call_kwargs = self.stream.client.make_request.call_args_list[0][1]
        sent_body = json.loads(list_call_kwargs.get("body", "{}"))
        self.assertEqual(sent_body, ALL_CUSTOMERS_FILTER)

    def test_content_type_header_forwarded_to_both_endpoints(self):
        """Content-Type: application/json must be present on every request after authenticate() fix."""
        self.stream.client.make_request.side_effect = [
            {"ids": ["x"], "next": None},
            {"customers": [{"id": "x"}]},
        ]

        list(self.stream.get_records())

        for idx, api_call in enumerate(self.stream.client.make_request.call_args_list):
            headers = api_call[0][3]
            self.assertIn(
                "Content-Type", headers,
                msg=f"Content-Type missing from call #{idx + 1}",
            )
            self.assertEqual(headers["Content-Type"], "application/json")


# ---------------------------------------------------------------------------
# Newsletters tests
# ---------------------------------------------------------------------------

class ConcreteNewsletters(Newsletters):
    """Concrete Newsletters with required abstract properties satisfied."""

    @property
    def tap_stream_id(self):
        return "newsletters"

    @property
    def replication_method(self):
        return "INCREMENTAL"

    @property
    def replication_keys(self):
        return ["updated"]

    @property
    def key_properties(self):
        return ["id"]


class TestNewslettersGetRecords(unittest.TestCase):
    """Tests for Newsletters.get_records() — verifies base-class pagination is used."""

    @patch("tap_customerio.streams.abstracts.metadata.to_map")
    def setUp(self, mock_to_map):
        mock_catalog = MagicMock()
        mock_catalog.schema.to_dict.return_value = {}
        mock_catalog.metadata = []
        mock_to_map.return_value = {}

        mock_client = MagicMock()
        mock_client.base_url = "https://api.customer.io/v1"

        self.stream = ConcreteNewsletters(client=mock_client, catalog=mock_catalog)
        # Simulate the bookmark filter that IncrementalStream.sync() sets via update_params()
        self.stream.params["updated_since"] = 1700000000

    def test_single_page_returns_all_records(self):
        """A response with no 'next' cursor yields records and stops."""
        self.stream.client.make_request.return_value = {
            "newsletters": [{"id": 1}, {"id": 2}],
        }

        records = list(self.stream.get_records())

        self.assertEqual(records, [{"id": 1}, {"id": 2}])
        self.assertEqual(self.stream.client.make_request.call_count, 1)

    def test_multi_page_yields_all_records_in_order(self):
        """Pagination across two pages yields records from both pages."""
        self.stream.client.make_request.side_effect = [
            {"newsletters": [{"id": 1}], "next": "cursor-page2"},
            {"newsletters": [{"id": 2}]},
        ]

        records = list(self.stream.get_records())

        self.assertEqual([r["id"] for r in records], [1, 2])
        self.assertEqual(self.stream.client.make_request.call_count, 2)

    def test_second_page_request_contains_start_cursor(self):
        """The 'next' value from page 1 must be sent as 'start' on page 2."""
        self.stream.client.make_request.side_effect = [
            {"newsletters": [{"id": 1}], "next": "cursor-abc"},
            {"newsletters": []},
        ]

        list(self.stream.get_records())

        second_call_params = self.stream.client.make_request.call_args_list[1][0][2]
        self.assertEqual(second_call_params.get("start"), "cursor-abc")

    def test_updated_since_bookmark_forwarded_to_api(self):
        """The updated_since param set via update_params() must be sent to the API."""
        self.stream.client.make_request.return_value = {"newsletters": []}

        list(self.stream.get_records())

        first_call_params = self.stream.client.make_request.call_args[0][2]
        self.assertIn("updated_since", first_call_params)
        self.assertEqual(first_call_params["updated_since"], 1700000000)

    def test_limit_param_is_sent(self):
        """The 'limit' page-size parameter must be present on every request."""
        self.stream.client.make_request.return_value = {"newsletters": []}

        list(self.stream.get_records())

        first_call_params = self.stream.client.make_request.call_args[0][2]
        self.assertIn("limit", first_call_params)
        self.assertEqual(first_call_params["limit"], self.stream.page_size)

    def test_falsy_next_cursor_terminates_pagination(self):
        """A None 'next' value must stop iteration after one page."""
        self.stream.client.make_request.return_value = {
            "newsletters": [{"id": 1}],
            "next": None,
        }

        records = list(self.stream.get_records())

        self.assertEqual(len(records), 1)
        self.assertEqual(self.stream.client.make_request.call_count, 1)

    @parameterized.expand([
        ["key_absent",   {}],
        ["key_is_null",  {"newsletters": None}],
        ["key_is_empty", {"newsletters": []}],
    ])
    def test_missing_or_null_data_key_returns_empty_list(self, name, response):
        """None or absent data_key must not raise TypeError and yields nothing."""
        self.stream.client.make_request.return_value = response

        records = list(self.stream.get_records())

        self.assertEqual(records, [])
