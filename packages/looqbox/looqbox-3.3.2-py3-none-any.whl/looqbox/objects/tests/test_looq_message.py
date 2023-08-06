import unittest
from looqbox.objects.looq_message import ObjMessage
from looqbox.objects.looq_message import LooqObject
import json


class TestObjMessage(unittest.TestCase):
    """
    Test looq_message file
    """

    def test_instance(self):
        looq_object_message = ObjMessage("Unit Test Text")

        self.assertIsInstance(looq_object_message, LooqObject)

    def test_json_creation(self):
        # Testing JSON without pass a new style
        looq_object_message = ObjMessage("Unit Test Text")

        json_keys = list(json.loads(looq_object_message.to_json_structure).keys())

        self.assertTrue("objectType" in json_keys, msg="objectType not found in JSON structure test 1")
        self.assertTrue("style" in json_keys, msg="style not found in JSON structure test 1")
        self.assertTrue("text" in json_keys, msg="text not found in JSON structure test 1")
        self.assertTrue("type" in json_keys, msg="type not found in JSON structure test 1")

        # Testing JSON with other style
        looq_object_message = ObjMessage("Unit Test Text", style={"background": "red", "color": "blue"})

        json_keys = list(json.loads(looq_object_message.to_json_structure).keys())

        self.assertTrue("objectType" in json_keys, msg="objectType not found in JSON structure test 2")
        self.assertTrue("style" in json_keys, msg="style not found in JSON structure test 2")
        self.assertTrue("text" in json_keys, msg="text not found in JSON structure test 2")
        self.assertTrue("type" in json_keys, msg="type not found in JSON structure test 2")
        

if __name__ == '__main__':
    unittest.main()
