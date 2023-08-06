import unittest
from looqbox.objects.looq_simple import ObjSimple
from looqbox.objects.looq_simple import LooqObject
import json


class TestObjSimple(unittest.TestCase):
    """
    Teste looq_simple file
    """
    def test_instance(self):
        looq_object_simple = ObjSimple("Unit Test Text")

        self.assertIsInstance(looq_object_simple, LooqObject)

    def test_json_creation(self):
        looq_object_simple = ObjSimple("Unit Test Text")

        json_keys = list(json.loads(looq_object_simple.to_json_structure).keys())

        self.assertTrue("objectType" in json_keys, msg="objectType not found in JSON structure test 1")
        self.assertTrue("text" in json_keys, msg="text not found in JSON structure test 1")

