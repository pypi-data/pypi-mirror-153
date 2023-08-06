import unittest
from looqbox.objects.looq_table import ObjTable
from looqbox.tools.tools import *
import pandas as pd
import numpy as np


class TestDataComp(unittest.TestCase):

    def test_data_comp(self):
        """
        Test data_comp function
        """
        # Normal Comparative
        table1 = ObjTable(data=pd.DataFrame({'Loja': ['SP', 'RJ', 'BH'],
                                             'Quantidade': [100, 310, 89],
                                             'Vendas': [2500, 5300, 1750]}))

        table1.total = {'Loja': 'Total',
                        'Quantidade': sum(table1.data['Quantidade']),
                        'Vendas': sum(table1.data['Vendas'])}

        table2 = ObjTable(data=pd.DataFrame({'Loja': ['SP', 'RJ', 'BH'],
                                             'Quantidade': [30, 400, 120],
                                             'Vendas': [950, 6000, 2200]}))

        table2.total = {'Loja': 'Total',
                        'Quantidade': sum(table2.data['Quantidade']),
                        'Vendas': sum(table2.data['Vendas'])}

        table = data_comp(table1, table2, by='Loja')

        self.assertEqual(pd.DataFrame({'Loja': ['SP', 'RJ', 'BH'],
                                       'Quantidade P1': table1.data['Quantidade'],
                                       'Quantidade P2': table2.data['Quantidade'],
                                       '∆%Quantidade': (table2.data['Quantidade'] / table1.data['Quantidade']) - 1,
                                       'Vendas P1': table1.data['Vendas'],
                                       'Vendas P2': table2.data['Vendas'],
                                       '∆%Vendas': (table2.data['Vendas'] / table1.data['Vendas']) - 1}).to_dict(),
                         table.data.to_dict(), msg="Error in normal comparative")

        self.assertEqual({'Loja': 'Total',
                          'Quantidade P1': sum(table1.data['Quantidade']),
                          'Quantidade P2': sum(table2.data['Quantidade']),
                          '∆%Quantidade': (sum(table2.data['Quantidade']) / sum(table1.data['Quantidade'])) - 1,
                          'Vendas P1': sum(table1.data['Vendas']),
                          'Vendas P2': sum(table2.data['Vendas']),
                          '∆%Vendas': (sum(table2.data['Vendas']) / sum(table1.data['Vendas'])) - 1
                          },
                         dict(table.total), msg="Error in normal total comparative")

        table1 = ObjTable(data=pd.DataFrame({'Loja': ['SP', 'RJ', 'BH', 'BA'],
                                             'Quantidade': [100, 310, 89, 30],
                                             'Vendas': [2500, 5300, 1750, 50]}))

        table1.total = {'Loja': 'Total',
                        'Quantidade': sum(table1.data['Quantidade']),
                        'Vendas': sum(table1.data['Vendas'])}

        table2 = ObjTable(data=pd.DataFrame({'Loja': ['SP', 'BA', 'BH'],
                                             'Quantidade': [30, 400, 120],
                                             'Vendas': [950, 6000, 2200]}))

        table2.total = {'Loja': 'Total',
                        'Quantidade': sum(table2.data['Quantidade']),
                        'Vendas': sum(table2.data['Vendas'])}

        table = data_comp(table1, table2, by='Loja')

        self.assertEqual(pd.DataFrame({'Loja': ['SP', 'RJ', 'BH', 'BA'],
                                       'Quantidade P1': [100, 310, 89, 30],
                                       'Quantidade P2': [30, "-", 120, 400],
                                       '∆%Quantidade': [-0.7, "-", 0.348314606741573, 12.333333333333334],
                                       'Vendas P1': [2500, 5300, 1750, 50],
                                       'Vendas P2': [950.0, "-", 2200.0, 6000.0],
                                       '∆%Vendas': [-0.62, "-", 0.2571428571428571, 119.0]}).to_dict(),
                         table.data.to_dict(), msg="Error in comparative with dataframe having differents rows")

        table1 = ObjTable(data=pd.DataFrame({'Loja': ['SP', 'RJ', 'BH', 'BA'],
                                             'Quantidade': [100, 0, 89, 30],
                                             'Vendas': [2500, 5300, 1750, 50]}))

        table1.total = {'Loja': 'Total',
                        'Quantidade': sum(table1.data['Quantidade']),
                        'Vendas': sum(table1.data['Vendas'])}

        table2 = ObjTable(data=pd.DataFrame({'Loja': ['SP', 'BA', 'BH'],
                                             'Quantidade': [30, 400, 120],
                                             'Vendas': [950, 6000, 2200]}))

        table2.total = {'Loja': 'Total',
                        'Quantidade': sum(table2.data['Quantidade']),
                        'Vendas': sum(table2.data['Vendas'])}

        table = data_comp(table1, table2, by='Loja')

        self.assertEqual(pd.DataFrame({'Loja': ['SP', 'RJ', 'BH', 'BA'],
                                       'Quantidade P1': [100, 0, 89, 30],
                                       'Quantidade P2': [30, "-", 120, 400],
                                       '∆%Quantidade': [-0.7, "-", 0.348314606741573, 12.333333333333334],
                                       'Vendas P1': [2500, 5300, 1750, 50],
                                       'Vendas P2': [950.0, "-", 2200.0, 6000.0],
                                       '∆%Vendas': [-0.62,"-", 0.2571428571428571, 119.0]}).to_dict(),
                         table.data.to_dict(), msg="Error in comparative with dataframe having differents rows")

    def test_transpose_data(self):
        """
        Test transpose_data function
        """
        table = ObjTable(data=pd.DataFrame({'Código': [2121], 'Preço': [25.70], 'Estoque': [21],
                                            'ABC Global': ['A1'], 'Tipo de Produto': ['OTC'],
                                            'Mg': [750], 'Fabricante': ['J & J'], 'Qtd.Comprimidos': [20]},
                                           columns=["Código", "Preço", "Estoque", "ABC Global", "Tipo de Produto",
                                                    "Mg", "Fabricante", "Qtd.Comprimidos"]))

        table.cell_format = {'Código': 'number:0', 'Preço': 'number:2', 'Estoque': 'number:0',
                              'Mg': 'number:0', 'Qtd.Comprimidos': 'number:0'}

        table.cell_style = {'Código': {'color': 'blue'}, 'Tipo de Produto': {'color': 'yellow'}}

        transposed_table = transpose_data(table, ['Atributo', 'Valor'])

        self.assertEqual(pd.DataFrame({'Atributo': ['Código', 'Preço', 'Estoque', 'ABC Global', 'Tipo de Produto', 'Mg',
                                                    'Fabricante', 'Qtd.Comprimidos'],
                                       'Valor': [2121, 25.7, 21, 'A1', 'OTC', 750, 'J & J', '20']}).all().all(),
                         transposed_table.data.all().all())

        self.assertDictEqual({'0': 'number:0', '1': 'number:2', '2': 'number:0', '5': 'number:0', '7': 'number:0'},
                             transposed_table.total_row_format)

        self.assertDictEqual({'0': {'color': 'blue'}, '4': {'color': 'yellow'}}, transposed_table.total_row_style)
