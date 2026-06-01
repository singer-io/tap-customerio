import copy
import os
import unittest
from datetime import datetime as dt
from datetime import timedelta

import dateutil.parser
import pytz
from tap_tester import connections, menagerie, runner
from tap_tester.logger import LOGGER
from tap_tester.base_suite_tests.base_case import BaseCase


class customerioBaseTest(BaseCase):
    """Setup expectations for test sub classes.

    Metadata describing streams. A bunch of shared methods that are used
    in tap-tester tests. Shared tap-specific methods (as needed).
    """
    start_date = "2019-01-01T00:00:00Z"
    IS_FORBIDDEN_STREAM = "is-forbidden-stream"

    @staticmethod
    def tap_name():
        """The name of the tap."""
        return "tap-customerio"

    @staticmethod
    def get_type():
        """The name of the tap."""
        return "platform.customerio"

    @classmethod
    def expected_metadata(cls):
        """The expected streams and metadata about the streams."""
        return {
            "broadcasts": {
                cls.PRIMARY_KEYS: { "id" },
                cls.REPLICATION_METHOD: cls.INCREMENTAL,
                cls.REPLICATION_KEYS: { "updated" },
                cls.RESPECTS_START_DATE: False,
                cls.API_LIMIT: 1
            },
            "transactional_messages": {
                cls.PRIMARY_KEYS: { "id" },
                cls.REPLICATION_METHOD: cls.INCREMENTAL,
                cls.REPLICATION_KEYS: { "updated_at" },
                cls.RESPECTS_START_DATE: True,
                cls.API_LIMIT: 1
            },
            "customers": {
                cls.PRIMARY_KEYS: { "id" },
                cls.REPLICATION_METHOD: cls.FULL_TABLE,
                cls.REPLICATION_KEYS: set(),
                cls.RESPECTS_START_DATE: False,
                cls.API_LIMIT: 1,
                cls.IS_FORBIDDEN_STREAM: True
            },
            "campaigns": {
                cls.PRIMARY_KEYS: { "id" },
                cls.REPLICATION_METHOD: cls.INCREMENTAL,
                cls.REPLICATION_KEYS: { "updated" },
                cls.RESPECTS_START_DATE: True,
                cls.API_LIMIT: 1
            },
            "newsletters": {
                cls.PRIMARY_KEYS: { "id" },
                cls.REPLICATION_METHOD: cls.INCREMENTAL,
                cls.REPLICATION_KEYS: { "updated" },
                cls.RESPECTS_START_DATE: True,
                cls.API_LIMIT: 1
            },
            "segments": {
                cls.PRIMARY_KEYS: { "id" },
                cls.REPLICATION_METHOD: cls.INCREMENTAL,
                cls.REPLICATION_KEYS: { "updated_at" },
                cls.RESPECTS_START_DATE: True,
                cls.API_LIMIT: 1
            },
            "messages": {
                cls.PRIMARY_KEYS: { "id" },
                cls.REPLICATION_METHOD: cls.FULL_TABLE,
                cls.REPLICATION_KEYS: set(),
                cls.RESPECTS_START_DATE: False,
                cls.API_LIMIT: 1
            },
            "exports": {
                cls.PRIMARY_KEYS: { "id" },
                cls.REPLICATION_METHOD: cls.INCREMENTAL,
                cls.REPLICATION_KEYS: { "updated_at" },
                cls.RESPECTS_START_DATE: False,
                cls.API_LIMIT: 1
            },
            "activities": {
                cls.PRIMARY_KEYS: { "id" },
                cls.REPLICATION_METHOD: cls.FULL_TABLE,
                cls.REPLICATION_KEYS: set(),
                cls.RESPECTS_START_DATE: False,
                cls.API_LIMIT: 1
            },
            "sender_identities": {
                cls.PRIMARY_KEYS: { "id" },
                cls.REPLICATION_METHOD: cls.FULL_TABLE,
                cls.REPLICATION_KEYS: set(),
                cls.RESPECTS_START_DATE: False,
                cls.API_LIMIT: 1
            },
            "reporting_webhooks": {
                cls.PRIMARY_KEYS: { "id" },
                cls.REPLICATION_METHOD: cls.FULL_TABLE,
                cls.REPLICATION_KEYS: set(),
                cls.RESPECTS_START_DATE: False,
                cls.API_LIMIT: 1
            },
            "snippets": {
                cls.PRIMARY_KEYS: { "name" },
                cls.REPLICATION_METHOD: cls.INCREMENTAL,
                cls.REPLICATION_KEYS: { "updated_at" },
                cls.RESPECTS_START_DATE: True,
                cls.API_LIMIT: 1
            },
            "info": {
                cls.PRIMARY_KEYS: { "ip_addresses" },
                cls.REPLICATION_METHOD: cls.FULL_TABLE,
                cls.REPLICATION_KEYS: set(),
                cls.RESPECTS_START_DATE: False,
                cls.API_LIMIT: 1
            },
            "collections": {
                cls.PRIMARY_KEYS: { "id" },
                cls.REPLICATION_METHOD: cls.INCREMENTAL,
                cls.REPLICATION_KEYS: { "updated_at" },
                cls.RESPECTS_START_DATE: False,
                cls.API_LIMIT: 1
            },
            "subscription_center": {
                cls.PRIMARY_KEYS: { "id" },
                cls.REPLICATION_METHOD: cls.FULL_TABLE,
                cls.REPLICATION_KEYS: set(),
                cls.RESPECTS_START_DATE: False,
                cls.API_LIMIT: 1
            },
            "workspaces": {
                cls.PRIMARY_KEYS: { "id" },
                cls.REPLICATION_METHOD: cls.FULL_TABLE,
                cls.REPLICATION_KEYS: set(),
                cls.RESPECTS_START_DATE: False,
                cls.API_LIMIT: 1
            },
            "objects": {
                cls.PRIMARY_KEYS: { "id" },
                cls.REPLICATION_METHOD: cls.FULL_TABLE,
                cls.REPLICATION_KEYS: set(),
                cls.RESPECTS_START_DATE: False,
                cls.API_LIMIT: 1
            },
            "eps_suppression": {
                cls.PRIMARY_KEYS: { "email" },
                cls.REPLICATION_METHOD: cls.FULL_TABLE,
                cls.REPLICATION_KEYS: set(),
                cls.RESPECTS_START_DATE: False,
                cls.API_LIMIT: 1
            }
        }

    @staticmethod
    def get_credentials():
        """Authentication information for the test account."""
        credentials_dict = {}
        creds = {'access_token': 'TAP_CUSTOMERIO_TOKEN'}

        for cred in creds:
            credentials_dict[cred] = os.getenv(creds[cred])

        return credentials_dict

    def get_properties(self, original: bool = True):
        """Configuration of properties required for the tap."""
        return {
            "start_date" : self.start_date
        }

    def expected_stream_names(self):
        """The expected stream names and exclude forbidden streams."""
        return {
            stream_name
            for stream_name, metadata in self.expected_metadata().items()
            if not metadata.get(self.IS_FORBIDDEN_STREAM, False)
        }

