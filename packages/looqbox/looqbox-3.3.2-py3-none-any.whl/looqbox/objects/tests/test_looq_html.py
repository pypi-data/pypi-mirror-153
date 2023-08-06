import unittest
from looqbox.objects.looq_html import ObjHTML
from looqbox.objects.looq_message import LooqObject
import json


class TestObjectHTML(unittest.TestCase):
    """
    Test looq_html file
    """

    def test_instance(self):
        looq_object_html = ObjHTML("<div> Unit Test Text <div>")

        self.assertIsInstance(looq_object_html, LooqObject)

    def test_json_creation(self):
        # Testing JSON keys
        looq_object_message = ObjHTML("<div> Unit Test Text <div>")

        json_keys = list(json.loads(looq_object_message.to_json_structure).keys())
        self.assertTrue("objectType" in json_keys, msg="objectType not found in JSON structure")
        self.assertTrue("html" in json_keys, msg="html not found in JSON structure")


if __name__ == '__main__':
    unittest.main()
