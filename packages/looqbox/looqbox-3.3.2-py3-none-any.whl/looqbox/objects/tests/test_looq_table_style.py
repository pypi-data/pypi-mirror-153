from looqbox.objects.tests import ObjTable
import pandas as pd
import numpy as np
import unittest
import json


def style_function(value=None):
    color = "rgb(76, 175, 80)"
    if value is None or value == "-":
        color = None
    elif value < 0.75:
        color = "rgb(183, 28, 28)"
    elif value < 0.9:
        color = "rgb(244, 67, 54)"
    elif value < 1:
        color = "rgb(255,140,0)"
    return {"color": color, "font-weight": "bold"}


class TestObjectTableStyle(unittest.TestCase):
    """
    Test looqbox table style attribute
    """

    def setUp(self) -> None:
        data = np.array([
            [100, 120, 98, 73, 20, 157, 124, 0, 9999, 100],
            [100, 100, 100, 100, 100, 100, 100, 100, 100, 100]
        ]).T

        df = pd.DataFrame(data, columns=['Venda', 'Meta'])
        df["Meta %"] = df["Venda"] / df["Meta"]
        self.looq_object_table = ObjTable(df)

    def test_value_style_with_function(self):
        looq_object_table = self.looq_object_table

        looq_object_table.value_style["Meta %"] = style_function

        table_json = json.loads(looq_object_table.to_json_structure)
        table_content = table_json["body"]["content"]
        for row in table_content:
            meta_perc = row["_lq_cell_config"]["Meta %"]
            self.assertTrue("style" in meta_perc.keys(), msg="style not found in table style function")

    def test_value_style_with_multiple_functions(self):
        looq_object_table = self.looq_object_table

        looq_object_table.value_style["Meta"] = style_function
        looq_object_table.value_style["Meta %"] = style_function

        table_json = json.loads(looq_object_table.to_json_structure)
        table_content = table_json["body"]["content"]
        for row in table_content:
            meta_perc = row["_lq_cell_config"]["Meta %"]
            self.assertTrue("style" in meta_perc.keys(), msg="style not found in table style function")

            meta = row["_lq_cell_config"]["Meta"]
            self.assertTrue("style" in meta.keys(), msg="style not found in table style function")

    def test_row_style(self):
        looq_object_table = self.looq_object_table
        looq_object_table.row_style = {
            0: {"color": "tomato"},
            8: {"color": "tomato"}
        }

        table_json = json.loads(looq_object_table.to_json_structure)
        table_content = table_json["body"]["content"]

        row_0_config = table_content[0]["_lq_row_config"]
        row_1_config = table_content[1]["_lq_row_config"]
        row_8_config = table_content[8]["_lq_row_config"]

        self.assertTrue("style" in row_0_config.keys(), msg="style not found on row 0")
        self.assertFalse("style" in row_1_config.keys(), msg="style found on row 1")
        self.assertTrue("style" in row_8_config.keys(), msg="style not found on row 8")

    def test_cell_style_with_function(self):
        looq_object_table = self.looq_object_table

        looq_object_table.cell_style["Meta %"] = style_function

        table_json = json.loads(looq_object_table.to_json_structure)
        table_content = table_json["body"]["content"]
        for row in table_content:
            meta_perc = row["_lq_cell_config"]["Meta %"]
            self.assertTrue("style" in meta_perc.keys(), msg="style not found in table style function")

    def test_cell_style_with_multiple_functions(self):
        looq_object_table = self.looq_object_table

        looq_object_table.cell_style["Meta"] = style_function
        looq_object_table.cell_style["Meta %"] = style_function

        table_json = json.loads(looq_object_table.to_json_structure)
        table_content = table_json["body"]["content"]
        for row in table_content:
            meta_perc = row["_lq_cell_config"]["Meta %"]
            self.assertTrue("style" in meta_perc.keys(), msg="style not found in table style function")

            meta = row["_lq_cell_config"]["Meta"]
            self.assertTrue("style" in meta.keys(), msg="style not found in table style function")


if __name__ == '__main__':
    unittest.main()
