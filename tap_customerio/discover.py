import re
import singer
from singer import metadata
from singer.catalog import Catalog, CatalogEntry, Schema
from tap_customerio.schema import get_schemas
from tap_customerio.streams import STREAMS
from tap_customerio.exceptions import customerioUnauthorizedError, customerioForbiddenError

LOGGER = singer.get_logger()


def discover(client=None) -> Catalog:
    """
    Run the discovery mode, prepare the catalog file and return the catalog.
    If a client is provided, each stream's endpoint is tested for accessibility.
    Streams that return HTTP 403 (Forbidden) are excluded from the catalog.
    HTTP 401 (Unauthorized) raises immediately as it indicates an invalid token.
    Any other error during probing is logged as a warning and the stream is
    included in the catalog, since permissions cannot be determined.
    """
    schemas, field_metadata = get_schemas()
    catalog = Catalog([])

    for stream_name, schema_dict in schemas.items():
        try:
            schema = Schema.from_dict(schema_dict)
            mdata = field_metadata[stream_name]
        except Exception as err:
            LOGGER.error(err)
            LOGGER.error("stream_name: {}".format(stream_name))
            LOGGER.error("type schema_dict: {}".format(type(schema_dict)))
            raise err

        if client is not None:
            stream_class = STREAMS.get(stream_name)
            if stream_class is not None:
                path = stream_class.path
                if "{" in path:
                    # Resolve template placeholders using class-level list attributes
                    # e.g. {suppression_type} -> suppression_types[0]
                    placeholders = re.findall(r'\{(\w+)\}', path)
                    fmt = {}
                    for ph in placeholders:
                        values = getattr(stream_class, ph + 's', None)
                        if isinstance(values, (list, tuple)) and values:
                            fmt[ph] = values[0]
                    if len(fmt) == len(placeholders):
                        path = path.format(**fmt)
                    else:
                        path = None  # Cannot resolve all placeholders, skip probing
                if path is not None:
                    try:
                        client.make_request(stream_class.http_method, "", params={"limit": 1}, path=path)
                    except customerioUnauthorizedError:
                        LOGGER.critical(
                            "Authentication failed during discovery for stream '%s': "
                            "invalid or expired access token.",
                            stream_name
                        )
                        raise
                    except customerioForbiddenError as err:
                        LOGGER.warning(
                            "Skipping stream '%s' from catalog: insufficient permissions (HTTP %s). Error: %s",
                            stream_name,
                            err.response.status_code if err.response is not None else "unknown",
                            err
                        )
                        continue
                    except Exception as err:
                        # Any other error (400, 404, 500, network, etc.) means we cannot
                        # determine permissions — include the stream in the catalog.
                        LOGGER.warning(
                            "Could not verify access for stream '%s' during discovery: %s. "
                            "Including in catalog.",
                            stream_name, err
                        )

        key_properties = metadata.to_map(mdata).get((), {}).get("table-key-properties")

        catalog.streams.append(
            CatalogEntry(
                stream=stream_name,
                tap_stream_id=stream_name,
                key_properties=key_properties,
                schema=schema,
                metadata=mdata,
            )
        )

    return catalog

