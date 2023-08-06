import unittest
from looqbox.integration.integration_links import get_partition


class TestGetPartition(unittest.TestCase):

    def test_get_partition_new_json_one_partition(self):
        """
        Test get_partition function with one partition in language version 2
        """
        par = {
            "question": {
                "residualWords": [
                    "venda"
                ],
                "original": "venda por dia $debug",
                "clean": "venda por dia esse mes",
                "residual": "venda "
            },
            "user": {
                "id": 41,
                "login": "gustavo",
                "groupId": 1,
                "language": "pt-br"
            },
            "entities": {
                "$date": {
                    "content": [
                        {
                            "segment": "esse mes",
                            "text": "esse mes",
                            "value": [
                                [
                                    "2021-01-01",
                                    "2021-01-31"
                                ]
                            ]
                        }
                    ]
                },
                "$datepartition": {
                    "content": [
                        {
                            "segment": "por dia",
                            "text": "por dia",
                            "value": [
                                "byDay"
                            ]
                        }
                    ]
                }
            },
            "partitions": {
                "$date": {
                    "content": [
                        {
                            "segment": "por dia",
                            "text": "por dia",
                            "value": [
                                "byDay"
                            ]
                        }
                    ]
                }
            },
            "companyId": 140,
            "apiVersion": 2,
            "keywords": [
                "venda",
                "por dia"
            ]
        }

        date_json = get_partition("$date", par)
        self.assertEqual([
            {"segment": "por dia", "text": "por dia", "value": ["byDay"]}
        ], date_json)

        store_json = get_partition("$store", par)
        self.assertEqual(None, store_json)

        default_value = get_partition("$undefined", par)
        self.assertIsNone(default_value)

    def test_get_partition_new_json(self):
        """
        Test get_partition function with multiple partitions in language version 2
        """
        par = {
            "question": {
                "residualWords": [
                    "venda"
                ],
                "original": "venda por loja por dia esse mes $debug",
                "clean": "venda por loja por dia esse mes",
                "residual": "venda "
            },
            "user": {
                "id": 41,
                "login": "gustavo",
                "groupId": 1,
                "language": "pt-br"
            },
            "entities": {
                "$date": {
                    "content": [
                        {
                            "segment": "esse mes",
                            "text": "esse mes",
                            "value": [
                                [
                                    "2021-01-01",
                                    "2021-01-31"
                                ]
                            ]
                        }
                    ]
                },
                "$datepartition": {
                    "content": [
                        {
                            "segment": "por dia",
                            "text": "por dia",
                            "value": [
                                "byDay"
                            ]
                        }
                    ]
                }
            },
            "partitions": {
                "$store": {
                    "content": [
                        {
                            "segment": "por loja",
                            "text": "por loja",
                            "value": [

                            ]
                        }
                    ]
                },
                "$date": {
                    "content": [
                        {
                            "segment": "por dia",
                            "text": "por dia",
                            "value": [
                                "byDay"
                            ]
                        }
                    ]
                }
            },
            "companyId": 140,
            "apiVersion": 2,
            "keywords": [
                "venda",
                "por loja",
                "por dia"
            ]
        }

        date = get_partition("$date", par)
        self.assertEqual([
            {"segment": "por dia", "text": "por dia", "value": ["byDay"]}
        ], date)

        mix_entities = get_partition(["$date", "$store"], par)
        self.assertEqual([
            {"segment": "por dia", "text": "por dia", "value": ["byDay"]},
            {"segment": "por loja", "text": "por loja", "value": []}
        ], mix_entities)


