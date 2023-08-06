from looqbox.objects.looq_object import LooqObject
from looqbox.json_encoder import JsonEncoder
from collections import OrderedDict
import json


class ObjQuery(LooqObject):

    def __init__(self, queries, total_time):
        super().__init__()
        self.queries = queries
        self.total_time = total_time

    @property
    def to_json_structure(self):
        json_content = OrderedDict(
            {
                "objectType": "query",
                "queries": self.queries,
                "totalTime": str(self.total_time)
            }
        )

        # Transforming in JSON
        queries_json = json.dumps(json_content, indent=1, allow_nan=True, cls=JsonEncoder)

        return queries_json
