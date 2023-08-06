import unittest
from looqbox.integration.integration_links import get_sso_attributes


class TestGetSsoAttributes(unittest.TestCase):

    def test_sso_attributes(self):
        """
        Test get_sso_attributes function
        """
        par = {
                "originalQuestion": "teste $debug",
                "cleanQuestion": "teste",
                "residualQuestion": "teste",
                "residualWords": [
                    "teste"
                ],
                "userlogin": "admin3",
                "userId": 725,
                "companyId": 84,
                "userGroupId": 1,
                "language": "pt-br",
                "apiVersion": 1,
                "userSsoAttributes": {
                    "Seguranca": [
                        "Group_1",
                        "group_two",
                        "G3"
                    ]
                },
                "keywords": [
                    "teste"
                ],
                "$residualWords": [
                    "teste"
                ]
            }

        par2 = {
            "question": {
                "residualWords": [
                    "teste"
                ],
                "original": "teste",
                "clean": "teste",
                "residual": "teste"
            },
            "user": {
                "id": 1,
                "login": "admin",
                "groupId": 1,
                "language": "pt-br",
                "ssoAttributes": {
                    "Seguranca": [
                        "Group_1",
                        "group_two",
                        "G3"
                    ]
                }
            },
            "entities": {},
            "partitions": {},
            "companyId": 0,
            "apiVersion": 2,
            "keywords": [
                "teste"
            ],
            "$query": False
        }

        self.assertEqual({"Seguranca": ["Group_1", "group_two", "G3"]}, get_sso_attributes(par))
        self.assertEqual({"Seguranca": ["Group_1", "group_two", "G3"]}, get_sso_attributes(par2))