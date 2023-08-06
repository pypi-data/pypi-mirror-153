from looqbox.objects.looq_object import LooqObject
from looqbox.json_encoder import JsonEncoder
from collections import OrderedDict
import json


class ObjList(LooqObject):

    def __init__(self, link_list=None, title=None):
        super().__init__()
        if link_list is None:
            link_list = []
        if title is None:
            title = []
        self.link_list = link_list
        self.title = title

    @property
    def to_json_structure(self):

        if not isinstance(self.title, list):
            self.title = [self.title]

        json_content = OrderedDict(
            {
                "objectType": "list",
                "title": self.title,
                "list": self.link_list
            }
        )

        # Transforming in JSON
        list_json = json.dumps(json_content, indent=1, allow_nan=True, cls=JsonEncoder)

        return list_json
