from looqbox.objects.tests import ObjForm
from looqbox.objects.tests import LooqObject
import unittest
import json
from collections import OrderedDict


class TestObjectForm(unittest.TestCase):
    """
    Test looq_form file
    """

    def test_instance(self):
        looq_object_form = ObjForm(
            {
                "type": "input", "label": "Loja", "value": "3",
                "name": "loja", "readonly": True
            },
            {
                "type": "input", "label": "Loja2",
                "value": "3", "name": "loja2", "readonly": True
            },
            title="Form"
        )

        self.assertIsInstance(looq_object_form, LooqObject)

    def test_json_creation(self):
        # Testing JSON keys

        looq_object_form = ObjForm(
            {
                "type": "input", "label": "Loja", "value": "3",
                "name": "loja", "readonly": True
            },
            {
                "type": "input", "label": "Loja2",
                "value": "3", "name": "loja2", "readonly": True
            },
            title="Form"
        )

        json_keys = list(json.loads(looq_object_form.to_json_structure, object_pairs_hook=OrderedDict).keys())
        self.assertTrue("objectType" in json_keys, msg="Key objectType not found in JSON structure")
        self.assertTrue("title" in json_keys, msg="Key title not found in JSON structure")
        self.assertTrue("method" in json_keys, msg="Key method not found in JSON structure")
        self.assertTrue("action" in json_keys, msg="Key action not found in JSON structure")
        self.assertTrue("filepath" in json_keys, msg="Key filepath not found in JSON structure")
        self.assertTrue("fields" in json_keys, msg="Key fields not found in JSON structure")


if __name__ == '__main__':
    unittest.main()
