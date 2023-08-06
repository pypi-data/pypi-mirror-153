from looqbox.objects.table_json_generator import TableJson
from looqbox.objects.table_json_generator import RowJson
from looqbox.objects.looq_object import LooqObject
from collections import OrderedDict
import pandas as pd


class TableFooter(LooqObject):
    def __init__(self, table_content=None, value_format=None, total=None, total_link=None, total_style=None,
                 total_tooltip=None, total_class=None, total_format=None, total_row_class=None, total_row_style=None,
                 total_row_format=None, total_row_link=None, total_row_tooltip=None, subtotal=None,
                 subtotal_format=None, subtotal_style=None, subtotal_link=None, subtotal_tooltip=None,
                 subtotal_class=None, subtotal_row_format=None, subtotal_row_style=None, subtotal_row_link=None,
                 subtotal_row_tooltip=None, subtotal_row_class=None, null_as=None, drill_text=None):

        super().__init__()
        self.table_content = table_content
        self.value_format = value_format
        self.total = total
        self.total_link = total_link
        self.total_class = total_class
        self.total_style = total_style
        self.total_tooltip = total_tooltip
        self.total_format = total_format
        self.total_row_class = total_row_class
        self.total_row_style = total_row_style
        self.total_row_format = total_row_format
        self.total_row_link = total_row_link
        self.total_row_tooltip = total_row_tooltip
        self.subtotal = subtotal
        self.subtotal_format = subtotal_format
        self.subtotal_link = subtotal_link
        self.subtotal_style = subtotal_style
        self.subtotal_tooltip = subtotal_tooltip
        self.subtotal_class = subtotal_class
        self.subtotal_row_format = subtotal_row_format
        self.subtotal_row_link = subtotal_row_link
        self.subtotal_row_style = subtotal_row_style
        self.subtotal_row_tooltip = subtotal_row_tooltip
        self.subtotal_row_class = subtotal_row_class
        self.null_as = null_as
        self.drill_text = drill_text

    def _get_footer_total(self, table_data, table_total, null_as):
        total_dict = OrderedDict()

        if isinstance(table_total, list):

            if len(table_total) != len(table_data.keys()):
                raise Exception('"Total" size is different from the number of columns. To use total this way, '
                                'please use a dictionary.')

            table_total_index = 0
            for key in table_data:
                total_dict[key] = table_total[table_total_index]
                table_total_index += 1

        elif isinstance(table_total, dict):
            for key in table_data.keys():
                total_dict[key] = table_total.get(key, null_as)
                if pd.isnull(total_dict[key]):
                    total_dict[key] = null_as

        for column in total_dict:

            element = {"value": total_dict[column],
                       "dataIndex": column,
                       }

            total_dict[column] = element

        return list(total_dict.values())

    def _add_total_index(self):
        self.total_row_style = {0: self.total_row_style}
        self.total_row_format = {0: self.total_row_format}
        self.total_row_link = {0: self.total_row_link}
        self.total_row_tooltip = {0: self.total_row_tooltip}

    @property
    def to_json_structure(self):

        table_total = self.total
        table_total_df = pd.DataFrame(table_total, self.table_content.columns).T
        table_data = self.table_content

        if len(self.subtotal) == table_data.shape[1] and not any(isinstance(sub, list) for sub in self.subtotal):
            table_subtotal = [self.subtotal]
        else:
            table_subtotal = self.subtotal

        if not isinstance(table_subtotal, list):
            raise Exception("Table subtotal must be a list of dictionaries")

        if isinstance(self.table_content, pd.DataFrame):
            table_data = table_data.to_dict(into=OrderedDict, orient='dict')

        if self.total_format is None and self.value_format is not None:
            self.total_format = self.value_format

        if self.subtotal_format is None and self.value_format is not None:
            self.subtotal_format = self.value_format

        # Build content
        total_list = self._get_footer_total(table_data, table_total, self.null_as)

        self._add_total_index()

        Total = TableJson(data=table_total_df,
                          cell_style=self.total_style,
                          cell_class=self.total_class,
                          cell_format=self.total_format,
                          cell_link=self.total_link,
                          cell_tooltip=self.total_tooltip,
                          drill_text=self.drill_text
                          )

        TotalRow = RowJson(data=table_total_df,
                           value_style=self.total_row_style,
                           value_class=self.total_row_class,
                           value_format=self.total_row_format,
                           value_link=self.total_row_link,
                           value_tooltip=self.total_row_tooltip)

        Subtotal = TableJson(data=self.table_content,
                             cell_style=self.subtotal_style,
                             cell_class=self.subtotal_class,
                             cell_format=self.subtotal_format,
                             cell_link=self.subtotal_link,
                             cell_tooltip=self.subtotal_tooltip)

        SubtotalRow = RowJson(data=self.table_content,
                              value_style=self.subtotal_row_style,
                              value_class=self.subtotal_row_class,
                              value_format=self.subtotal_row_format,
                              value_link=self.subtotal_row_link,
                              value_tooltip=self.subtotal_row_tooltip)
        # Total and Subtotal
        total_cell_config = dict()

        for column in table_data:
            #  Default attribute values for each column
            total_cell_config[column] = {
                "class": None,
                "style": None,
                "format": None,
                "tooltip": None,
                "drill": None,
                "drillText": None
            }

            # Total always have 1 line, so index is 0
            total_cell_config = Total.cell_config(total_cell_config, column, idx=0)

        total_row_config = TotalRow.row_config(0, Total)

        subtotal_idx = 0
        subtotal_json_content = list()
        for subtotal in table_subtotal:

            subtotal_cell_config = dict()
            if isinstance(subtotal, dict):
                subtotal_content = [dict(value=value, dataIndex=col) for value, col in subtotal.items()]

            elif isinstance(subtotal, list):

                if len(subtotal) == len(self.table_content.columns):
                    columns = self.table_content.columns
                    subtotal_content = [dict(value=subtotal[idx], dataIndex=columns[idx])
                                        for idx in range(len(columns))]

                else:
                    raise Exception("Table subtotal must have the same number of elements as the table")

                for column in table_data:
                    subtotal_cell_config[column] = {
                        "class": None,
                        "style": None,
                        "format": None,
                        "tooltip": None,
                        "drill": None
                    }

                    subtotal_cell_config.update(
                        Subtotal.cell_config(subtotal_cell_config, column, subtotal_idx)
                    )

            subtotal_row_config = SubtotalRow.row_config(subtotal_idx, Subtotal)

            subtotal_dict = {
                "content": subtotal_content,
                "_lq_cell_config": subtotal_cell_config,
                "_lq_row_config": subtotal_row_config
            }

            subtotal_json_content.append(subtotal_dict)
            subtotal_idx += 1

        # Create footer json
        footer_json = {"content": total_list, "_lq_cell_config": total_cell_config, "_lq_row_config": total_row_config,
                       "subtotal": subtotal_json_content}

        return footer_json
