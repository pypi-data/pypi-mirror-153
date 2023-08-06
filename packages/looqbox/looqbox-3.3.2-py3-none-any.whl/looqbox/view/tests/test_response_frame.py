import unittest
from looqbox.view.response_board import ResponseFrame
from looqbox.objects.looq_message import ObjMessage
from looqbox.objects.looq_message import LooqObject
import json
from collections import OrderedDict


class TestResponseFrame(unittest.TestCase):
    """
    Test response_frame file
    """

    def test_instance(self):
        frame = ResponseFrame()

        self.assertIsInstance(frame, LooqObject, msg="Error in object hierarchy")

    def test_content_integrity(self):
        test_message = ObjMessage("test text")

        # Testing if content is a list
        frame_test_1 = ResponseFrame(content=[test_message])
        self.assertIs(frame_test_1.content.__class__, list, msg="Error in content with correct type")

        frame_test_2 = ResponseFrame(content=test_message)
        self.assertIsNot(frame_test_2.content.__class__, list, msg="Error in content with incorrect type")

        frame_test_3 = ResponseFrame()
        self.assertIs(frame_test_3.content.__class__, list, msg="Error in default content type")

    def test_json_creation(self):
        # Testing JSON without pass a new style
        test_message = ObjMessage("Unit Test Text")
        frame = ResponseFrame()

        expected_json = OrderedDict(
            {
                'type': 'frame',
                'class': [],
                'content': [],
                'style': None,
                'stacked': True,
                'title': None,
                'tabView': False,
                'insights': None
            }
        )

        frame_json = json.loads(frame.to_json_structure)
        self.assertEqual(expected_json.keys(), frame_json.keys(), msg="Failed basic JSON structure test")

        # Testing JSON with other style
        frame = ResponseFrame(content=[test_message])

        expected_json = OrderedDict(
            {
                'type': 'frame',
                'class': [],
                'content': [json.loads(test_message.to_json_structure)],
                'style': None,
                'stacked': True,
                'title': None,
                'tabView': False,
                'insights': None
            }
        )

        frame_json = json.loads(frame.to_json_structure)
        self.assertEqual(expected_json.keys(), frame_json.keys(), msg="JSON test failed with more than one style")


if __name__ == '__main__':
    unittest.main()
