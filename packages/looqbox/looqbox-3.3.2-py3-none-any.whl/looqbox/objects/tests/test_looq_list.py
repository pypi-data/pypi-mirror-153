from looqbox.objects.tests import ObjList
from looqbox.objects.tests import LooqObject
from collections import OrderedDict
import unittest
import json


class TestObjectList(unittest.TestCase):
    """
    Test looq_list file
    """

    def test_instance(self):
        looq_object_list = ObjList("test", "test fake")

        self.assertIsInstance(looq_object_list, LooqObject)

    def test_json_creation(self):
        # Testing JSON keys
        looq_object_list = ObjList("test", "test fake")

        json_keys = list(json.loads(looq_object_list.to_json_structure, object_pairs_hook=OrderedDict).keys())
        self.assertTrue("objectType" in json_keys, msg="objectType not found in JSON structure")
        self.assertTrue("title" in json_keys, msg="title not found in JSON structure")
        self.assertTrue("list" in json_keys, msg="list not found in JSON structure")


if __name__ == '__main__':
    unittest.main()
