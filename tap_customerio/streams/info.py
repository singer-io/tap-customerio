from typing import Any, Dict, Tuple, List, Iterator
from tap_customerio.streams.abstracts import FullTableStream


class Info(FullTableStream):
    tap_stream_id = "info"
    key_properties = ["id"]
    replication_method = "FULL_TABLE"
    replication_keys = []
    data_key = "ip_addresses"
    path = "info/ip_addresses"

    def modify_object(self, record: List, parent_record: Dict = None) -> Dict:
        """
        Modify the record before writing to the stream
        """
        rec = dict()
        rec["ip_addresses"] = record
        return rec

