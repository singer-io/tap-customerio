# tap-customerio

This is a [Singer](https://singer.io) tap that produces JSON-formatted data
following the [Singer
spec](https://github.com/singer-io/getting-started/blob/master/docs/SPEC.md).

This tap:

- Pulls raw data from the [customerio API].
- Extracts the following resources:
    - [Broadcasts](https://docs.customer.io/integrations/api/app/#operation/listBroadcasts)

    - [TransactionalMessages](https://docs.customer.io/integrations/api/app/#tag/Transactional)

    - [Customers](https://docs.customer.io/integrations/api/app/#tag/Customers)

    - [Campaigns](https://docs.customer.io/integrations/api/app/#tag/Campaigns)

    - [Newsletters](https://docs.customer.io/integrations/api/app/#tag/Newsletters)

    - [Segments](https://docs.customer.io/integrations/api/app/#tag/Snippets)

    - [Messages](https://docs.customer.io/integrations/api/app/#tag/Messages)

    - [Exports](https://docs.customer.io/integrations/api/app/#tag/Exports)

    - [Activities](https://docs.customer.io/integrations/api/app/#tag/Activities)

    - [SenderIdentities](https://docs.customer.io/integrations/api/app/#tag/Sender-Identities)

    - [ReportingWebhooks](https://docs.customer.io/integrations/api/app/#tag/Reporting-Webhooks)

    - [Snippets](https://docs.customer.io/integrations/api/app/#tag/Snippets)

    - [Info](https://docs.customer.io/integrations/api/app/#tag/Info)

    - [Collections](https://docs.customer.io/integrations/api/app/#tag/Collections)

    - [SubscriptionCenter](https://docs.customer.io/integrations/api/app/#tag/Subscription-Center)

    - [Workspaces](https://docs.customer.io/integrations/api/app/#tag/Workspaces)

    - [Objects](https://docs.customer.io/integrations/api/app/#tag/Objects)

    - [EpsSuppression](https://docs.customer.io/integrations/api/app/#tag/ESP-Suppression)

- Outputs the schema for each resource
- Incrementally pulls data based on the input state


## Streams


**[broadcasts](https://docs.customer.io/integrations/api/app/#operation/listBroadcasts)**
- Data Key = broadcasts
- Primary keys: ['id']
- replication_keys = ["updated"]
- Replication strategy: INCREMENTAL

**[transactional_messages](https://docs.customer.io/integrations/api/app/#tag/Transactional)**
- Data Key = messages
- Primary keys: ['id']
- replication_keys = ["updated_at"]
- Replication strategy: INCREMENTAL

**[customers](https://docs.customer.io/integrations/api/app/#tag/Customers)**
- Data Key = customers
- Primary keys: ['id']
- replication_keys = [ ]
- Replication strategy: FULL_TABLE

**[campaigns](https://docs.customer.io/integrations/api/app/#tag/Campaigns)**
- Data Key = campaigns
- Primary keys: ['id']
- replication_keys = ["updated"]
- Replication strategy: INCREMENTAL

**[newsletters](https://docs.customer.io/integrations/api/app/#tag/Newsletters)**
- Data Key = newsletters
- Primary keys: ['id']
- replication_keys = ["updated"]
- Replication strategy: INCREMENTAL

**[segments](https://docs.customer.io/integrations/api/app/#tag/Snippets)**
- Data Key = segments
- Primary keys: ['id']
- replication_keys = ["updated_at"
- Replication strategy: INCREMENTAL

**[messages](https://docs.customer.io/integrations/api/app/#tag/Messages)**
- Data Key = messages
- Primary keys: ['id']
- replication_keys = []
- Replication strategy: FULL_TABLE

**[exports](https://docs.customer.io/integrations/api/app/#tag/Exports)**
- Data Key = exports
- Primary keys: ['id']
- replication_keys = ["updated_at"]
- Replication strategy: INCREMENTAL

**[activities](https://docs.customer.io/integrations/api/app/#tag/Activities)**
- Data Key = activities
- Primary keys: ['id']
- replication_keys = [ ]
- Replication strategy: FULL_TABLE

**[sender_identities](https://docs.customer.io/integrations/api/app/#tag/Sender-Identities)**
- Data Key = sender_identities
- Primary keys: ['id']
- replication_keys = [ ]
- Replication strategy: FULL_TABLE

**[reporting_webhooks](https://docs.customer.io/integrations/api/app/#tag/Reporting-Webhooks)**
- Data Key = reporting_webhooks
- Primary keys: ['id']
- replication_keys = [ ]
- Replication strategy: FULL_TABLE

**[snippets](https://docs.customer.io/integrations/api/app/#tag/Snippets)**
- Data Key = snippets
- Primary keys: ['name']
- replication_keys = ['updated_at']
- Replication strategy: INCREMENTAL

**[info](https://docs.customer.io/integrations/api/app/#tag/Info)**
- Data Key = ip_addresses
- Primary keys: ['ip_addresses']
- replication_keys = [ ]
- Replication strategy: FULL_TABLE

**[collections](https://docs.customer.io/integrations/api/app/#tag/Collections)**
- Data Key = collections
- Primary keys: ['id']
- replication_keys = ['updated_at']
- Replication strategy: INCREMENTAL

**[subscription_center](https://docs.customer.io/integrations/api/app/#tag/Subscription-Center)**
- Data Key = topics
- Primary keys: ['id']
- replication_keys = [ ]
- Replication strategy: FULL_TABLE

**[workspaces](https://docs.customer.io/integrations/api/app/#tag/Workspaces)**
- Data Key = Workspaces
- Primary keys: ['id']
- replication_keys = [ ]
- Replication strategy: FULL_TABLE

**[objects](https://docs.customer.io/integrations/api/app/#tag/Objects)**
- Data Key = types
- Primary keys: ['id']
- replication_keys = [ ]
- Replication strategy: FULL_TABLE

**[eps_suppression](https://docs.customer.io/integrations/api/app/#tag/ESP-Suppression)**
- Data Key = suppressions
- Primary keys: ['email']
- replication_keys = [ ]
- Replication strategy: FULL_TABLE



## Authentication

## Quick Start

1. Install

    Clone this repository, and then install using setup.py. We recommend using a virtualenv:

    ```bash
    > virtualenv -p python3 venv
    > source venv/bin/activate
    > python setup.py install
    OR
    > cd .../tap-customerio
    > pip install -e .
    ```
2. Dependent libraries. The following dependent libraries were installed.
    ```bash
    > pip install singer-python
    > pip install target-stitch
    > pip install target-json

    ```
    - [singer-tools](https://github.com/singer-io/singer-tools)
    - [target-stitch](https://github.com/singer-io/target-stitch)

3. Create your tap's `config.json` file.  The tap config file for this tap should include these entries:
   - `start_date` - the default value to use if no bookmark exists for an endpoint (rfc3339 date string)
   - `user_agent` (string, optional): Process and email for API logging purposes. Example: `tap-customerio <api_user_email@your_company.com>`
   - `request_timeout` (integer, `300`): Max time for which request should wait to get a response. Default request_timeout is 300 seconds.

    ```json
    {
        "start_date": "2019-01-01T00:00:00Z",
        "user_agent": "tap-customerio <api_user_email@your_company.com>",
        "request_timeout": 300
    }
   ```

    Optionally, also create a `state.json` file. `currently_syncing` is an optional attribute used for identifying the last object to be synced in case the job is interrupted mid-stream. The next run would begin where the last job left off.

    ```json
    {
        "currently_syncing": "engage",
        "bookmarks": {
            "export": "2019-09-27T22:34:39.000000Z",
            "funnels": "2019-09-28T15:30:26.000000Z",
            "revenue": "2019-09-28T18:23:53Z"
        }
    }
    ```

4. Run the Tap in Discovery Mode
    This creates a catalog.json for selecting objects/fields to integrate:
    ```bash
    tap-customerio --config config.json --discover > catalog.json
    ```
   See the Singer docs on discovery mode
   [here](https://github.com/singer-io/getting-started/blob/master/docs/DISCOVERY_MODE.md#discovery-mode).

5. Run the Tap in Sync Mode (with catalog) and [write out to state file](https://github.com/singer-io/getting-started/blob/master/docs/RUNNING_AND_DEVELOPING.md#running-a-singer-tap-with-a-singer-target)

    For Sync mode:
    ```bash
    > tap-customerio --config tap_config.json --catalog catalog.json > state.json
    > tail -1 state.json > state.json.tmp && mv state.json.tmp state.json
    ```
    To load to json files to verify outputs:
    ```bash
    > tap-customerio --config tap_config.json --catalog catalog.json | target-json > state.json
    > tail -1 state.json > state.json.tmp && mv state.json.tmp state.json
    ```
    To pseudo-load to [Stitch Import API](https://github.com/singer-io/target-stitch) with dry run:
    ```bash
    > tap-customerio --config tap_config.json --catalog catalog.json | target-stitch --config target_config.json --dry-run > state.json
    > tail -1 state.json > state.json.tmp && mv state.json.tmp state.json
    ```

6. Test the Tap
    While developing the customerio tap, the following utilities were run in accordance with Singer.io best practices:
    Pylint to improve [code quality](https://github.com/singer-io/getting-started/blob/master/docs/BEST_PRACTICES.md#code-quality):
    ```bash
    > pylint tap_customerio -d missing-docstring -d logging-format-interpolation -d too-many-locals -d too-many-arguments
    ```
    Pylint test resulted in the following score:
    ```bash
    Your code has been rated at 9.67/10
    ```

    To [check the tap](https://github.com/singer-io/singer-tools#singer-check-tap) and verify working:
    ```bash
    > tap_customerio --config tap_config.json --catalog catalog.json | singer-check-tap > state.json
    > tail -1 state.json > state.json.tmp && mv state.json.tmp state.json
    ```

    #### Unit Tests

    Unit tests may be run with the following.

    ```
    python -m pytest --verbose
    ```

    Note, you may need to install test dependencies.

    ```
    pip install -e .'[dev]'
    ```
---

Copyright &copy; 2019 Stitch
