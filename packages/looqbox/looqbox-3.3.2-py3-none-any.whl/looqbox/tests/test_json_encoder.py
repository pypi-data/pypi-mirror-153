from looqbox.json_encoder import JsonEncoder
import numpy as np
import datetime
import unittest
import json


class TestJsonEncoder(unittest.TestCase):
    """
    Test JsonEncoder object conversion
    """

    def test_numpy_conversion(self):

        test_dict = {
            "numpyInt64": np.int64(42),
            "numpyFloat64": np.float64(4.2),
            "numpyArray": np.array([1, 2, 3]),
            "nan": np.nan
        }

        test_json = json.dumps(test_dict, allow_nan=True, cls=JsonEncoder)

        self.assertTrue("numpyInt64" in test_json, msg="numpyInt64 not found in JSON conversion test")
        self.assertTrue("numpyFloat64" in test_json, msg="numpyFloat64 not found in JSON conversion test")
        self.assertTrue("numpyArray" in test_json, msg="numpyArray not found in JSON conversion test")
        self.assertTrue("nan" in test_json, msg="nan not found in JSON conversion test")

    def test_datetime_conversion(self):

        test_dict = {
            "datetime": datetime.datetime.now(),
            "date": datetime.date.today()
        }

        test_json = json.dumps(test_dict, allow_nan=True, cls=JsonEncoder)

        self.assertTrue("datetime" in test_json, msg="datetime not found in JSON conversion test")
        self.assertTrue("date" in test_json, msg="date not found in JSON conversion test")


if __name__ == '__main__':
    unittest.main()
