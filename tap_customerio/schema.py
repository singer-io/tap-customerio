import os
import json
import singer
from typing import Dict, Tuple
from singer import metadata
from tap_customerio.streams import STREAMS
from tap_customerio.exceptions import customerioUnauthorizedError, customerioForbiddenError

LOGGER = singer.get_logger()


def _resolve_probe_path(stream_class):
    """
    Returns a concrete probe path for the stream class.
    For templated paths, uses the first value from suppression_types.
    """
    if stream_class.suppression_types:
        return stream_class.path.format(suppression_type=stream_class.suppression_types[0])
    return stream_class.path


def has_stream_access(client, stream_name, stream_class):
    """
    Probes the stream endpoint to verify access permissions.

    Returns True if accessible, False on HTTP 403 (stream excluded from catalog).
    Raises immediately on HTTP 401 (invalid token).
    All other exceptions propagate unchanged.

    For GET streams, a lightweight request with limit=1 is used.
    For POST streams, the stream's probe_body is sent as a minimal valid request.
    """
    probe_path = _resolve_probe_path(stream_class)
    try:
        if stream_class.http_method == "GET":
            client.make_request("GET", "", params={"limit": 1}, path=probe_path)
        else:
            client.make_request(
                stream_class.http_method,
                "",
                headers={"Content-Type": "application/json"},
                body=json.dumps(stream_class.probe_body or {}),
                path=probe_path,
            )
        return True
    except customerioUnauthorizedError as ex:
        raise Exception(
            "Authentication failed during discovery for stream '%s': "
            "invalid or expired access token.",
            stream_name
        ) from ex
    except customerioForbiddenError as err:
        LOGGER.warning(
            "Skipping stream '%s' from catalog: insufficient permissions (HTTP %s). Error: %s",
            stream_name,
            err.response.status_code if err.response is not None else "unknown",
            err
        )
        return False


def get_abs_path(path: str) -> str:
    """
    Get the absolute path for the schema files.
    """
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), path)


def load_schema_references() -> Dict:
    """
    Load the schema files from the schema folder and return the schema references.
    """
    shared_schema_path = get_abs_path("schemas/shared")

    shared_file_names = []
    if os.path.exists(shared_schema_path):
        shared_file_names = [
            f
            for f in os.listdir(shared_schema_path)
            if os.path.isfile(os.path.join(shared_schema_path, f))
        ]

    refs = {}
    for shared_schema_file in shared_file_names:
        with open(os.path.join(shared_schema_path, shared_schema_file)) as data_file:
            refs["shared/" + shared_schema_file] = json.load(data_file)

    return refs


def get_schemas(client) -> Tuple[Dict, Dict]:
    """
    Load the schema references, prepare metadata for each stream and return
    schema and metadata for the catalog.
    Each stream's endpoint is probed for access; streams returning HTTP 403 are excluded.
    """
    schemas = {}
    field_metadata = {}

    refs = load_schema_references()
    for stream_name, stream_obj in STREAMS.items():
        if not has_stream_access(client, stream_name, stream_obj):
            continue

        schema_path = get_abs_path("schemas/{}.json".format(stream_name))
        with open(schema_path) as file:
            schema = json.load(file)

        schemas[stream_name] = schema
        schema = singer.resolve_schema_references(schema, refs)

        mdata = metadata.new()
        mdata = metadata.get_standard_metadata(
            schema=schema,
            key_properties=getattr(stream_obj, "key_properties"),
            valid_replication_keys=(getattr(stream_obj, "replication_keys") or []),
            replication_method=getattr(stream_obj, "replication_method"),
        )
        mdata = metadata.to_map(mdata)

        automatic_keys = getattr(stream_obj, "replication_keys") or []
        # print(automatic_keys, stream_name, schema)
        for field_name in schema.get("properties", {}).keys():
            if field_name in automatic_keys:
                mdata = metadata.write(
                    mdata, ("properties", field_name), "inclusion", "automatic"
                )

        mdata = metadata.to_list(mdata)
        field_metadata[stream_name] = mdata

    return schemas, field_metadata
