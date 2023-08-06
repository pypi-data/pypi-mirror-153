import unittest
from looqbox.utils.utils import *
from looqbox.objects.looq_table import ObjTable
import pandas as pd
import datetime


class TestUtils(unittest.TestCase):
    #
    # def test_title_with_date(self):
    #     """
    #     Test title_with_date function
    #     """
    #
    #     date_1 = ['2019-01-01', '2019-01-01']
    #     date_2 = ['2018-12-10', '2018-12-16']
    #     date_3 = ['2018-01-01', '2018-01-31']
    #     date_4 = ['2018-01-01', '2018-12-31']
    #
    #     self.assertEqual('Período  dia  01/01/2019',
    #                      title_with_date('Período', date_1, "pt-br"))
    #
    #     self.assertEqual('Período  de  10/12/2018 a 16/12/2018',
    #                      title_with_date('Período', date_2, "pt-br"))
    #
    #     self.assertEqual('Período  de  01/01/2018 a 31/01/2018',
    #                      title_with_date('Período', date_3, "pt-br"))
    #
    #     self.assertEqual('Período  de  01/01/2018 a 31/12/2018',
    #                      title_with_date('Período', date_4, "pt-br"))

    def test_format_cnpj(self):
        """
        Test format_cnpj function
        """

        self.assertEqual('00.100.000/0100-01',
                         format_cnpj('0100000010001'))

    def test_format_cpf(self):
        """
        Test format_cpf function
        """

        self.assertEqual('001.001.001-01',
                         format_cpf('00100100101'))

    # def test_format(self):
    #     """
    #     Test format function
    #     """
    #
    #     self.assertEqual('2.500,00', format(2500, 'number:2'))
    #     self.assertEqual('2.500,0', format(2500, 'number:1'))
    #     self.assertEqual('2.500', format(2500, 'number:0'))
    #     self.assertEqual('85.53%', format(0.8553, 'percent:2'))
    #     self.assertEqual('85.5%', format(0.8553, 'percent:1'))
    #     self.assertEqual('86%', format(0.8553, 'percent:0'))
    #     self.assertEqual('01/01/2018', format(pd.to_datetime('2018-01-01'), 'date'))
    #     self.assertEqual('01/01/2018', format(pd.to_datetime('2018-01-01'), 'Date'))
    #     self.assertEqual('01/01/2018 05:02:00', format(pd.to_datetime('2018-01-01 05:02:00'), 'datetime'))
    #     self.assertEqual('01/01/2018 05:02:00', format(pd.to_datetime('2018-01-01 05:02:00'), 'Datetime'))

    def test_drill_if(self):
        """
        Test drill_if function
        """

        table = ObjTable()
        stores = ['Sao Paulo', 'LooqCity', 'Chicago', 'Roma', 'Tokio',
                  'Belem', 'Berlin', 'New York', 'Franca', 'London']
        codes = range(0, 10)

        table.data = pd.DataFrame({"Codigo": list(codes), "Loja": stores,
                                   "Venda": [200, 580, 965, 753, 134, 741, 156, 452, 764, 1000]},
                                  columns=["Codigo", "Loja", "Venda"])

        table.cell_link = {
            "Venda": "testando",
            "Loja": [table.create_droplist({"text": "Head", "link": "Teste da meta da loja {}"},
                                           [table.data["Loja"]]),
                     table.create_droplist({"text": "Head 2", "link": "Teste da meta da loja {}"},
                                           [table.data["Loja"]])]
        }

        self.assertEqual([[{'text': 'Head', 'link': 'Teste da meta da loja Sao Paulo'},
                           {'text': 'Head', 'link': 'Teste da meta da loja LooqCity'},
                           {'text': 'Head', 'link': 'Teste da meta da loja Chicago'},
                           {'text': 'Head', 'link': 'Teste da meta da loja Roma'},
                           {'text': 'Head', 'link': 'Teste da meta da loja Tokio'},
                           {'text': 'Head', 'link': 'Teste da meta da loja Belem'},
                           {'text': 'Head', 'link': 'Teste da meta da loja Berlin'},
                           {'text': 'Head', 'link': 'Teste da meta da loja New York'},
                           {'text': 'Head', 'link': 'Teste da meta da loja Franca'},
                           {'text': 'Head', 'link': 'Teste da meta da loja London'}]],
                         drill_if(table.cell_link["Loja"], [None, 1]))

        table.cell_link = {
            "Venda": "testando",
            "Loja": [table.create_droplist({"text": "Head", "link": "Teste da meta da loja {}"},
                                           [table.data["Loja"]]),
                     table.create_droplist({"text": "Head 2", "link": "Teste da meta da loja {}"},
                                           [table.data["Loja"]])]
        }

        self.assertEqual([[{'text': 'Head 2', 'link': 'Teste da meta da loja Sao Paulo'},
                           {'text': 'Head 2', 'link': 'Teste da meta da loja LooqCity'},
                           {'text': 'Head 2', 'link': 'Teste da meta da loja Chicago'},
                           {'text': 'Head 2', 'link': 'Teste da meta da loja Roma'},
                           {'text': 'Head 2', 'link': 'Teste da meta da loja Tokio'},
                           {'text': 'Head 2', 'link': 'Teste da meta da loja Belem'},
                           {'text': 'Head 2', 'link': 'Teste da meta da loja Berlin'},
                           {'text': 'Head 2', 'link': 'Teste da meta da loja New York'},
                           {'text': 'Head 2', 'link': 'Teste da meta da loja Franca'},
                           {'text': 'Head 2', 'link': 'Teste da meta da loja London'}]],
                         drill_if(table.cell_link["Loja"], [1, None]))

        table.cell_link = {
            "Venda": "testando",
            "Loja": [table.create_droplist({"text": "Head", "link": "Teste da meta da loja {}"},
                                           [table.data["Loja"]]),
                     table.create_droplist({"text": "Head 2", "link": "Teste da meta da loja {}"},
                                           [table.data["Loja"]])]
        }

        self.assertEqual(None, drill_if(table.cell_link["Loja"], [1, 1]))

        table.cell_link = {
            "Venda": "testando",
            "Loja": [table.create_droplist({"text": "Head", "link": "Teste da meta da loja {}"},
                                           [table.data["Loja"]]),
                     table.create_droplist({"text": "Head 2", "link": "Teste da meta da loja {}"},
                                           [table.data["Loja"]])]
        }

        self.assertEqual([[{'text': 'Head', 'link': 'Teste da meta da loja Sao Paulo'},
                           {'text': 'Head', 'link': 'Teste da meta da loja LooqCity'},
                           {'text': 'Head', 'link': 'Teste da meta da loja Chicago'},
                           {'text': 'Head', 'link': 'Teste da meta da loja Roma'},
                           {'text': 'Head', 'link': 'Teste da meta da loja Tokio'},
                           {'text': 'Head', 'link': 'Teste da meta da loja Belem'},
                           {'text': 'Head', 'link': 'Teste da meta da loja Berlin'},
                           {'text': 'Head', 'link': 'Teste da meta da loja New York'},
                           {'text': 'Head', 'link': 'Teste da meta da loja Franca'},
                           {'text': 'Head', 'link': 'Teste da meta da loja London'}],
                          [{'text': 'Head 2', 'link': 'Teste da meta da loja Sao Paulo'},
                           {'text': 'Head 2', 'link': 'Teste da meta da loja LooqCity'},
                           {'text': 'Head 2', 'link': 'Teste da meta da loja Chicago'},
                           {'text': 'Head 2', 'link': 'Teste da meta da loja Roma'},
                           {'text': 'Head 2', 'link': 'Teste da meta da loja Tokio'},
                           {'text': 'Head 2', 'link': 'Teste da meta da loja Belem'},
                           {'text': 'Head 2', 'link': 'Teste da meta da loja Berlin'},
                           {'text': 'Head 2', 'link': 'Teste da meta da loja New York'},
                           {'text': 'Head 2', 'link': 'Teste da meta da loja Franca'},
                           {'text': 'Head 2', 'link': 'Teste da meta da loja London'}]],
                         drill_if(table.cell_link["Loja"], [None, None]))

        table.cell_link = {
            "Venda": "testando",
            "Loja": [table.create_droplist({"text": "Head", "link": "Teste da meta da loja {}"},
                                           [table.data["Loja"]]),
                     table.create_droplist({"text": "Head 2", "link": "Teste da meta da loja {}"},
                                           [table.data["Loja"]])]
        }

        self.assertEqual(None, drill_if(table.cell_link["Venda"], 1))

    def test_current_day(self):
        """
        Test current_day function
        """

        self.assertEqual(
            [datetime.datetime.now().strftime("%Y-%m-%d"),
             datetime.datetime.now().strftime("%Y-%m-%d")],
            current_day('date'))
        self.assertEqual(
            [datetime.datetime.now().strftime("%Y-%m-%d"),
             datetime.datetime.now().strftime("%Y-%m-%d")],
            current_day())
        self.assertEqual([datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                          datetime.datetime.now().strftime("%Y-%m-%d %H:%M")],
                         current_day('datetime'))
        self.assertEqual(
            [datetime.datetime.now().strftime("%Y-%m-%d"),
             datetime.datetime.now().strftime("%Y-%m-%d")],
            current_day('Date'))
        self.assertEqual([datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                          datetime.datetime.now().strftime("%Y-%m-%d %H:%M")],
                         current_day('DateTime'))
        self.assertEqual([datetime.datetime.now().strftime("%Y-%m-%d"),
                          datetime.datetime.now().strftime("%Y-%m-%d")],
                         current_day('kjhsdfj'))

    def test_partition(self):
        """
        Test current_day function
        """

        self.assertEqual([["foo", "foo"]], partition("foo"))
        self.assertEqual([["foo", 1]], partition(["foo", 1]))
        self.assertEqual([["foo", 5], [5, True]], partition(["foo", 5, True]))
        self.assertEqual([["foo", 5], [5, True], [True, "goo"]], partition(["foo", 5, True, "goo"]))

