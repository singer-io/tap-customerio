# tap-customerio

This is a [Singer](https://singer.io) tap that produces JSON-formatted data
following the [Singer
spec](https://github.com/singer-io/getting-started/blob/master/docs/SPEC.md).

This tap:

- Pulls raw data from the [customerio API].
- Extracts the following resources:
    - [Broadcasts](https://fly.customer.io/workspaces/196173/journeys/home)

    - [Transactional](https://fly.customer.io/workspaces/196173/journeys/home)

    - [Customers](https://fly.customer.io/workspaces/196173/journeys/home)

    - [Campaigns](https://fly.customer.io/workspaces/196173/journeys/home)

    - [Newsletters](https://help.getharvest.com/api-v2/invoices-api/invoices/invoices/)

    - [Segments](https://help.getharvest.com/api-v2/invoices-api/invoices/invoices/)

    - [Messages](https://help.getharvest.com/api-v2/invoices-api/invoices/invoices/)

    - [Exports](https://help.getharvest.com/api-v2/invoices-api/invoices/invoices/)

    - [Activities](https://help.getharvest.com/api-v2/invoices-api/invoices/invoices/)

    - [SenderIdentities](https://help.getharvest.com/api-v2/invoices-api/invoices/invoices/)

    - [ReportingWebhooks](https://help.getharvest.com/api-v2/invoices-api/invoices/invoices/)

    - [Snippets](https://help.getharvest.com/api-v2/invoices-api/invoices/invoices/)

    - [Info](https://help.getharvest.com/api-v2/invoices-api/invoices/invoices/)

    - [Collections](https://help.getharvest.com/api-v2/invoices-api/invoices/invoices/)

    - [Imports](https://help.getharvest.com/api-v2/invoices-api/invoices/invoices/)

    - [SubscriptionCenter](https://help.getharvest.com/api-v2/invoices-api/invoices/invoices/)

    - [Workspaces](https://www.postman.com/galactic-resonance-157195/customer-io-apis/request/ez0g7z2/list-workspaces)

    - [Objects](https://help.getharvest.com/api-v2/invoices-api/invoices/invoices/)

    - [EpsSuppression](https://help.getharvest.com/api-v2/invoices-api/invoices/invoices/)

- Outputs the schema for each resource
- Incrementally pulls data based on the input state


## Streams


**[broadcasts](https://fly.customer.io/workspaces/196173/journeys/home)**
- Data Key = broadcasts
- Primary keys: ['id']
- Replication strategy: INCREMENTAL

**[transactional](https://fly.customer.io/workspaces/196173/journeys/home)**
- Data Key = messages
- Primary keys: ['id']
- Replication strategy: INCREMENTAL

**[customers](https://fly.customer.io/workspaces/196173/journeys/home)**
- Data Key = customers
- Primary keys: ['id']
- Replication strategy: INCREMENTAL

**[campaigns](https://fly.customer.io/workspaces/196173/journeys/home)**
- Data Key = campaigns
- Primary keys: ['id']
- Replication strategy: INCREMENTAL

**[newsletters](https://help.getharvest.com/api-v2/invoices-api/invoices/invoices/)**
- Data Key = newsletters
- Primary keys: ['id']
- Replication strategy: INCREMENTAL

**[segments](https://help.getharvest.com/api-v2/invoices-api/invoices/invoices/)**
- Data Key = segments
- Primary keys: ['id']
- Replication strategy: INCREMENTAL

**[messages](https://help.getharvest.com/api-v2/invoices-api/invoices/invoices/)**
- Data Key = messages
- Primary keys: ['id']
- Replication strategy: FULL_TABLE

**[exports](https://help.getharvest.com/api-v2/invoices-api/invoices/invoices/)**
- Data Key = exports
- Primary keys: ['id']
- Replication strategy: INCREMENTAL

**[activities](https://help.getharvest.com/api-v2/invoices-api/invoices/invoices/)**
- Data Key = activities
- Primary keys: ['id']
- Replication strategy: FULL_TABLE

**[sender_identities](https://help.getharvest.com/api-v2/invoices-api/invoices/invoices/)**
- Data Key = sender_identities
- Primary keys: ['id']
- Replication strategy: FULL_TABLE

**[reporting_webhooks](https://help.getharvest.com/api-v2/invoices-api/invoices/invoices/)**
- Data Key = reporting_webhooks
- Primary keys: ['id']
- Replication strategy: INCREMENTAL

**[snippets](https://help.getharvest.com/api-v2/invoices-api/invoices/invoices/)**
- Data Key = snippets
- Primary keys: ['snippet_name']
- Replication strategy: INCREMENTAL

**[info](https://help.getharvest.com/api-v2/invoices-api/invoices/invoices/)**
- Data Key = ip_addresses
- Primary keys: ['id']
- Replication strategy: FULL_TABLE

**[collections](https://help.getharvest.com/api-v2/invoices-api/invoices/invoices/)**
- Data Key = collections
- Primary keys: ['id']
- Replication strategy: INCREMENTAL

**[imports](https://help.getharvest.com/api-v2/invoices-api/invoices/invoices/)**
- Data Key = import
- Primary keys: ['id']
- Replication strategy: INCREMENTAL

**[subscription_center](https://help.getharvest.com/api-v2/invoices-api/invoices/invoices/)**
- Data Key = topics
- Primary keys: ['id']
- Replication strategy: FULL_TABLE

**[workspaces](https://www.postman.com/galactic-resonance-157195/customer-io-apis/request/ez0g7z2/list-workspaces)**
- Data Key = Workspaces
- Primary keys: ['id']
- Replication strategy: FULL_TABLE

**[objects](https://help.getharvest.com/api-v2/invoices-api/invoices/invoices/)**
- Data Key = types
- Primary keys: ['id']
- Replication strategy: FULL_TABLE

**[eps_suppression](https://help.getharvest.com/api-v2/invoices-api/invoices/invoices/)**
- Data Key = suppressions
- Primary keys: ['id']
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
    }```

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
