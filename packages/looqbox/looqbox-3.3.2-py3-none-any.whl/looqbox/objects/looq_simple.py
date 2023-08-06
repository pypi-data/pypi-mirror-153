from looqbox.objects.looq_object import LooqObject
from looqbox.json_encoder import JsonEncoder
import json


class ObjSimple(LooqObject):
    """
    Create an object to be used inside a looq.objSimple. The goal of this object is to
    send a JSON to be used inside IoT, wearables and assistants.
    """
    def __init__(self, text):
        """
        :param text: Text to be showed in the device.
        """
        super().__init__()
        self.text = text


    @property
    def to_json_structure(self):
        """
        Creates the JSON structure to be read by the FES.

        :return: A JSON string.
        """

        json_content = {
            "objectType": "simple",
            "text": self.text
        }

        # Transforming in JSON
        simple_json = json.dumps(json_content, indent=1, allow_nan=True, cls=JsonEncoder)

        return simple_json