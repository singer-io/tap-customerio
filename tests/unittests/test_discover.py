import unittest
from unittest.mock import MagicMock

from tap_customerio.discover import discover
from tap_customerio.schema import has_stream_access
from tap_customerio.exceptions import (
    customerioForbiddenError,
    customerioUnauthorizedError,
    customerioBadRequestError,
)
from tap_customerio.streams.customers import Customers


def _make_client(side_effect=None):
    client = MagicMock()
    if side_effect is not None:
        client.make_request.side_effect = side_effect
    return client


class TestDiscoverWithClient(unittest.TestCase):
    """discover() with a client returns all accessible streams."""

    def test_returns_all_streams_when_all_accessible(self):
        client = _make_client(side_effect=None)
        catalog = discover(client=client)
        self.assertIsNotNone(catalog)
        self.assertGreater(len(catalog.streams), 0)


class TestDiscoverProbing(unittest.TestCase):
    """discover() with a client probes each stream endpoint."""

    def test_stream_included_on_successful_probe(self):
        client = _make_client(side_effect=None)  # no error -> success
        catalog = discover(client=client)
        stream_names = {s.stream for s in catalog.streams}
        self.assertIn("campaigns", stream_names)

    def test_stream_excluded_on_403(self):
        forbidden_response = MagicMock()
        forbidden_response.status_code = 403
        forbidden_err = customerioForbiddenError("HTTP-error-code: 403", forbidden_response)

        def side_effect(method, endpoint=None, params=None, path=None, **kwargs):
            if path == "campaigns":
                raise forbidden_err
            # all other streams succeed

        client = _make_client(side_effect=side_effect)
        catalog = discover(client=client)
        stream_names = {s.stream for s in catalog.streams}
        self.assertNotIn("campaigns", stream_names)

    def test_non_permission_error_reraises(self):
        bad_request_response = MagicMock()
        bad_request_response.status_code = 400
        bad_request_err = customerioBadRequestError("HTTP-error-code: 400", bad_request_response)

        def side_effect(method, endpoint=None, params=None, path=None, **kwargs):
            if path == "campaigns":
                raise bad_request_err

        client = _make_client(side_effect=side_effect)
        # 400 is not a permission error — it re-raises and does not silently include the stream
        with self.assertRaises(customerioBadRequestError):
            discover(client=client)

    def test_401_raises_immediately(self):
        unauthorized_response = MagicMock()
        unauthorized_response.status_code = 401
        unauthorized_err = customerioUnauthorizedError("HTTP-error-code: 401", unauthorized_response)

        client = _make_client(side_effect=unauthorized_err)
        with self.assertRaises(Exception) as ctx:
            discover(client=client)
        self.assertIsInstance(ctx.exception.__cause__, customerioUnauthorizedError)

    def test_eps_suppression_included_on_successful_probe(self):
        """eps_suppression path is templated; it should be probed with first suppression_type."""
        client = _make_client(side_effect=None)
        catalog = discover(client=client)
        stream_names = {s.stream for s in catalog.streams}
        self.assertIn("eps_suppression", stream_names)

    def test_eps_suppression_excluded_on_403(self):
        forbidden_response = MagicMock()
        forbidden_response.status_code = 403
        forbidden_err = customerioForbiddenError("HTTP-error-code: 403", forbidden_response)

        def side_effect(method, endpoint=None, params=None, path=None, **kwargs):
            if path == "esp/suppression/bounces":
                raise forbidden_err

        client = _make_client(side_effect=side_effect)
        catalog = discover(client=client)
        stream_names = {s.stream for s in catalog.streams}
        self.assertNotIn("eps_suppression", stream_names)

    def test_multiple_streams_excluded_on_403(self):
        forbidden_response = MagicMock()
        forbidden_response.status_code = 403
        forbidden_err = customerioForbiddenError("HTTP-error-code: 403", forbidden_response)

        restricted = {"campaigns", "broadcasts"}

        def side_effect(method, endpoint=None, params=None, path=None, **kwargs):
            if path in restricted:
                raise forbidden_err

        client = _make_client(side_effect=side_effect)
        catalog = discover(client=client)
        stream_names = {s.stream for s in catalog.streams}
        for stream in restricted:
            self.assertNotIn(stream, stream_names)

    def test_customers_stream_probed_with_post_method(self):
        """customers stream (POST) must be probed using POST with probe_body, not skipped."""
        import json
        client = _make_client()
        catalog = discover(client=client)
        stream_names = {s.stream for s in catalog.streams}
        self.assertIn("customers", stream_names)
        # Verify the probe used POST to customers/attributes with probe_body
        matched = [
            call for call in client.make_request.call_args_list
            if call.kwargs.get("path") == "customers/attributes"
        ]
        self.assertTrue(matched, "Expected a probe call to customers/attributes")
        self.assertEqual(matched[0].args[0], "POST")
        self.assertEqual(json.loads(matched[0].kwargs.get("body", "{}")), {"ids": []})

    def test_customers_stream_excluded_on_403(self):
        """customers stream is excluded from catalog when POST probe returns 403."""
        forbidden_response = MagicMock()
        forbidden_response.status_code = 403
        forbidden_err = customerioForbiddenError("HTTP-error-code: 403", forbidden_response)

        def side_effect(method, endpoint=None, params=None, path=None, **kwargs):
            if path == "customers/attributes" and method == "POST":
                raise forbidden_err

        client = _make_client(side_effect=side_effect)
        catalog = discover(client=client)
        stream_names = {s.stream for s in catalog.streams}
        self.assertNotIn("customers", stream_names)

    def test_has_stream_access_uses_post_for_post_stream(self):
        """has_stream_access probes POST streams using POST + probe_body."""
        import json
        client = _make_client()
        result = has_stream_access(client, "customers", Customers)
        self.assertTrue(result)
        client.make_request.assert_called_once()
        call = client.make_request.call_args
        self.assertEqual(call.args[0], "POST")
        self.assertEqual(call.kwargs.get("path"), "customers/attributes")
        self.assertEqual(json.loads(call.kwargs.get("body", "{}")), {"ids": []})


if __name__ == "__main__":
    unittest.main()
