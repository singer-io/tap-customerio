from tap_customerio.streams.broadcasts import Broadcasts
from tap_customerio.streams.transactional import Transactional
from tap_customerio.streams.customers import Customers
from tap_customerio.streams.campaigns import Campaigns
from tap_customerio.streams.newsletters import Newsletters
from tap_customerio.streams.segments import Segments
from tap_customerio.streams.messages import Messages
from tap_customerio.streams.exports import Exports
from tap_customerio.streams.activities import Activities
from tap_customerio.streams.sender_identities import SenderIdentities
from tap_customerio.streams.reporting_webhooks import ReportingWebhooks
from tap_customerio.streams.snippets import Snippets
from tap_customerio.streams.info import Info
from tap_customerio.streams.collections import Collections
from tap_customerio.streams.imports import Imports
from tap_customerio.streams.subscription_center import SubscriptionCenter
from tap_customerio.streams.workspaces import Workspaces
from tap_customerio.streams.objects import Objects
from tap_customerio.streams.eps_suppression import EpsSuppression

STREAMS = {
    "broadcasts": Broadcasts,
    "transactional": Transactional,
    "customers": Customers,
    "campaigns": Campaigns,
    "newsletters": Newsletters,
    "segments": Segments,
    "messages": Messages,
    "exports": Exports,
    "activities": Activities,
    "sender_identities": SenderIdentities,
    "reporting_webhooks": ReportingWebhooks,
    "snippets": Snippets,
    "info": Info,
    "collections": Collections,
    "imports": Imports,
    "subscription_center": SubscriptionCenter,
    "workspaces": Workspaces,
    "objects": Objects,
    "eps_suppression": EpsSuppression,
}

