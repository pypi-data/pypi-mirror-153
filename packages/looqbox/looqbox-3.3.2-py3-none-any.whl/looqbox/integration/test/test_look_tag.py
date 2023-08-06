import unittest
from looqbox.integration.integration_links import look_tag


class TestLookTag(unittest.TestCase):

    def setUp(self) -> None:
        self.par_v1 = {
            "originalQuestion": "teste",
            "cleanQuestion": "teste",
            "residualQuestion": "",
            "residualWords": [""],
            "entityDictionary": None,
            "userlogin": "user",
            "userId": 666,
            "companyId": 0,
            "userGroupId": 0,
            "language": "pt-br",
            "$date": [
                [
                    "2019-01-08",
                    "2019-01-08"
                ]
            ],
            "$datetime": [
                [
                    "2019-01-08 00:00:00",
                    "2019-01-08 00:00:00"
                ]
            ],
            "$store": [1, 2, 3, 4, 5, 6, 7, 8],
            "apiVersion": 1
        }

        self.par_v2 = {
            "question": {
                "residualWords": [
                    "meta",
                    "python"
                ],
                "original": "meta python $debug",
                "clean": "meta python",
                "residual": "meta python"
            },
            "user": {
                "id": 1101,
                "login": "matheus",
                "groupId": 1,
                "language": "pt-br"
            },
            "entities": {
                "$store": {
                    "content": [
                        {
                            "segment": "da loja sao paulo",
                            "value": [
                                1
                            ]
                        }
                    ]
                },
                "$date": {
                    "content": [
                        {
                            "segment": "hoje",
                            "text": "hoje",
                            "value": [
                                [
                                    "2020-01-22",
                                    "2020-01-22"
                                ]
                            ]
                        }
                    ]
                }
            },
            "partitions": {

            },
            "companyId": 0,
            "apiVersion": 2,
            "keywords": [
                "meta",
                "python"
            ]
        }

    def test_look_tag_json_v2_one_entity(self):
        """
        Test look_tag function with one entity in language version 2
        """

        par = self.par_v2

        date = look_tag("$date", par)
        self.assertEqual([['2020-01-22', '2020-01-22']], date)

        default_value = look_tag("$undefined", par)
        self.assertEqual(None, default_value)

    def test_look_tag_json_v2(self):
        """
        Test look_tag function with multiple entities in language version 2
        """

        par = self.par_v2

        date = look_tag("$date", par)
        self.assertEqual([['2020-01-22', '2020-01-22']], date)

        mix_entities = look_tag(["$date", "$store"], par)
        self.assertEqual([
            [['2020-01-22', '2020-01-22']],
            [1]
        ], mix_entities)

    def test_look_tag_json_v1(self):
        """
        Test look_tag function in language version 1
        """

        par = self.par_v1

        date_value = look_tag("$date", par)
        self.assertEqual([['2019-01-08', '2019-01-08']], date_value)

        store_value = look_tag("$store", par)
        self.assertEqual([1, 2, 3, 4, 5, 6, 7, 8], store_value)

        default_value = look_tag("$undefined", par)
        self.assertIsNone(default_value)

        mix_value = look_tag(["$date", "$datetime"], par)
        self.assertEqual([['2019-01-08', '2019-01-08'], ['2019-01-08 00:00:00', '2019-01-08 00:00:00']], mix_value)

    def test_look_tag_json_v2_default_value(self):
        """
        Test look_tag function with one entity in language version 2
        """
        par = self.par_v2

        date = look_tag("$entity", par, [['2020-01-22', '2020-01-22']])
        self.assertEqual([['2020-01-22', '2020-01-22']], date)

        store = look_tag("$entity", par, [1])
        self.assertEqual([1], store)

        default_value = look_tag("$undefined", par)
        self.assertIsNone(default_value)
